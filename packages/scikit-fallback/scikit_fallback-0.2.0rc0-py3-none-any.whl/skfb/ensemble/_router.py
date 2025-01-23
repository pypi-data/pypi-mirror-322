"""Routing classifiers."""

__all__ = ("RoutingClassifier",)

import warnings

import numpy as np

from sklearn.base import BaseEstimator, check_is_fitted, ClassifierMixin, clone
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import check_cv
from sklearn.utils.multiclass import unique_labels

try:
    from sklearn.utils.parallel import delayed, Parallel
except ModuleNotFoundError:
    from joblib import Parallel

    # pylint: disable=ungrouped-imports
    from sklearn.utils.fixes import delayed

from ..utils._legacy import (
    _fit_context,
    HasMethods,
    Integral,
    Interval,
    StrOptions,
    validate_params,
)
from ._common import fit_one


class RouterWarning(UserWarning):
    """Warns about inconsistency in labels produced for fitting routers."""


class RoutingClassifier(BaseEstimator, ClassifierMixin):
    """Learns a deferral rule to switch between base estimators in an ensemble.

    Trains all estimators and a router. The router is fed w/ the validation features
    and the deferral labels - indices of the estimators that have correct predictions.
    During inference, predicts estimator indices using the router and passes the
    corresponding samples to the estimators for final predictions.

    Parameters
    ----------
    estimators : array-like of object, length n_estimators
        Base estimators. Preferrably, from weakest (e.g., rule-based or linear) to
        strongest (e.g., gradient boosting).
    router : object
        Router estimator.
    when_error : {"prefer_weaker", "prefer_stronger"}, default="prefer_weaker"
        Whether to choose the first (weaker) estimator during training when all the
        estimators make mistakes.
    when_true : {"prefer_weaker", "prefer_stronger"}, default="prefer_weaker"
        Whether to choose a weaker estimator during training when there is more than
        one estimator giving the correct answer.
    cv : int, cross-validation generator or an iterable, default=None
        The cross-validation splitting strategy.
        Splits data into pairs - for ``estimators`` and ``router`` - only once.
        Defaults to stratified 80/20 split.
        Possible inputs for cv are:

        - None, to use the efficient Leave-One-Out cross-validation
        - integer, to specify the number of folds.
        - :term:`CV splitter`,
        - An iterable yielding (train, test) splits as arrays of indices.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`~sklearn.model_selection.StratifiedKFold` is used.
    n_jobs : int, default=None
        Number of parallel jobs used during training.
    verbose : int, default=0
        Verbosity level.
    """

    _parameter_constraints = {
        "estimators": ["array-like"],
        "router": [HasMethods(["fit", "predict"])],
        "when_error": [StrOptions({"prefer_weaker", "prefer_stronger"})],
        "when_true": [StrOptions({"prefer_weaker", "prefer_stronger"})],
        "cv": ["cv_object"],
        "n_jobs": [Interval(Integral, -1, None, closed="left"), None],
        "verbose": ["verbose"],
    }

    def __init__(
        self,
        estimators,
        router,
        when_error="prefer_weaker",
        when_true="prefer_weaker",
        cv=None,
        n_jobs=None,
        verbose=0,
    ):
        self.estimators = estimators
        self.router = router
        self.when_error = when_error
        self.when_true = when_true
        self.cv = cv
        self.n_jobs = n_jobs
        self.verbose = verbose

    @_fit_context(prefer_skip_nested_validation=False)
    @validate_params(
        {
            "X": ["array-like", "sparse matrix"],
            "y": ["array-like"],
            "sample_weight": ["array-like", None],
        },
        prefer_skip_nested_validation=True,
    )
    def fit(self, X, y, sample_weight=None):
        """Trains all estimators and routing classifier.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,) or (n_samples, n_outputs)
            The target values (class labels).
        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted.

        Returns
        -------
        self : object
            Returns self.
        """
        self.classes_ = unique_labels(y)

        # region Split (X, y, sample_weight) into train & val
        self.cv_ = check_cv(cv=self.cv, y=y, classifier=True)
        train_idx, val_idx = next(self.cv_.split(X, y=y))
        X_train, y_train = X[train_idx], y[train_idx]
        X_val, y_val = X[val_idx], y[val_idx]
        if sample_weight is not None:
            sample_weight_train = sample_weight[train_idx]
        else:
            sample_weight_train = sample_weight
        # endregion

        # region Train estimators
        self.estimators_ = Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(
            delayed(fit_one)(estimator, X_train, y_train, sample_weight_train)
            for estimator in self.estimators
        )
        self.estimators_ = np.array(self.estimators_, dtype=object)
        # endregion

        # region Form labels for router
        Y_pred = Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(
            delayed(estimator.predict)(X_val)
            for estimator in self.estimators_
        )
        y_mask = Y_pred == y_val
        y_choose = np.apply_along_axis(self._choose_model_index, 0, y_mask)
        # endregion

        # region Train router
        unique, count = np.unique(y_choose, return_counts=True)
        print(unique, count)

        if min(count) < 2:
            warnings.warn(
                "Not every estimator will be chosen by router",
                category=RouterWarning,
            )

        while min(count) < 2:
            out_label = unique[np.argmin(count)]
            mask = y_choose != out_label
            X_val = X_val[mask]
            y_choose = y_choose[mask]
            unique, count = np.unique(y_choose, return_counts=True)

        if len(unique) == 1:
            warnings.warn(
                "Only one estimator was chosen for fitting router",
                category=RouterWarning,
            )

            self.router_ = DummyClassifier(strategy="constant", constant=unique[0])
            self.router_.fit(X_val, y_choose)
        else:
            self.router_ = clone(self.router).fit(X_val, y_choose)
        # endregion

        self.is_fitted_ = True

        return self

    @validate_params(
        {
            "X": ["array-like", "sparse matrix"],
        },
        prefer_skip_nested_validation=True,
    )
    def predict(self, X):
        """Predits w/ one of the estimators chosen by the routing classifier.

        Parameters
        ----------
        X : indexable, length n_samples
            Input samples to classify.
            Must fulfill the input assumptions of the underlying estimators.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Classes predicted by the base estimators.
        """
        check_is_fitted(self, attributes="is_fitted_")

        y_defer = self.router_.predict(X)
        print(np.unique(y_defer, return_counts=True))
        y_pred = np.zeros(len(X), dtype=self.classes_.dtype)
        defer_unique = unique_labels(y_defer)
        M = y_defer == defer_unique.reshape(-1, 1)
        for i, est_label in enumerate(defer_unique):
            mask = M[i]
            y_pred[mask] = self.estimators_[est_label].predict(X[mask, :])

        return y_pred

    @validate_params(
        {
            "X": ["array-like", "sparse matrix"],
        },
        prefer_skip_nested_validation=True,
    )
    def decision_function(self, X):
        """Predits decision scores w/ one of the estimators chosen by the router.

        Parameters
        ----------
        X : indexable, length n_samples
            Input samples to classify.
            Must fulfill the input assumptions of the underlying estimators.

        Returns
        -------
        y_score : ndarray of shape (n_samples,)
            Scores predicted by the base estimators.
        """
        check_is_fitted(self, attributes="is_fitted_")

        y_defer = self.router_.predict(X)
        y_score = np.zeros(len(X), dtype=np.float64)
        defer_unique = unique_labels(y_defer)
        M = y_defer == defer_unique.reshape(-1, 1)
        for i, est_label in enumerate(defer_unique):
            mask = M[i]
            y_score[mask] = self.estimators_[est_label].decision_function(X[mask, :])

        return y_score

    @validate_params(
        {
            "X": ["array-like", "sparse matrix"],
        },
        prefer_skip_nested_validation=True,
    )
    def predict_proba(self, X):
        """Predicts probabilities using an estimator chosen by the router.

        Parameters
        ----------
        X : indexable, length n_samples
            Input samples to classify.
            Must fulfill the input assumptions of the underlying estimators.

        Returns
        -------
        y_prob : ndarray of shape (n_samples, n_classes)
            Probabilities predicted by the base estimators.
        """
        check_is_fitted(self, attributes="is_fitted_")

        y_defer = self.router_.predict(X)
        Y_prob = np.zeros((len(X), len(self.classes_)), dtype=np.float64)
        defer_unique = unique_labels(y_defer)
        M = y_defer == defer_unique.reshape(-1, 1)
        for i, est_label in enumerate(defer_unique):
            mask = M[i]
            Y_prob[mask] = self.estimators_[est_label].predict_proba(X[mask, :])

        return Y_prob

    @validate_params(
        {
            "X": ["array-like", "sparse matrix"],
        },
        prefer_skip_nested_validation=True,
    )
    def predict_log_proba(self, X):
        """Predicts log-probabilities using an estimator chosen by the router.

        Parameters
        ----------
        X : indexable, length n_samples
            Input samples to classify.
            Must fulfill the input assumptions of the underlying estimators.

        Returns
        -------
        y_score : ndarray of shape (n_samples, n_classes)
            Log-probabilities predicted by the base estimators.
        """
        return np.log(self.predict_proba(X))

    @validate_params(
        {
            "X": ["array-like", "sparse matrix"],
            "y": ["array-like"],
            "sample_weight": ["array-like", None],
        },
        prefer_skip_nested_validation=True,
    )
    def score(self, X, y, sample_weight=None):
        """Computes accuracy score on true labels and cascade predictions.

        Parameters
        ----------
        X : indexable, length n_samples
            Input samples to evaluate.
            Must fulfill the input assumptions of the underlying estimators.
        y : array-like of shape (n_samples,)
            True labels for `X`.
        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted.

        Returns
        -------
        score : float
            Accuracy score.
        """
        check_is_fitted(self, attributes="is_fitted_")

        return accuracy_score(y, self.predict(X), sample_weight=sample_weight)

    def _choose_model_index(self, acc_mask):
        """Chooses the index of a model from an accuracy mask."""
        accuracy = acc_mask.sum()
        if accuracy == 0:
            if self.when_error == "prefer_weaker":
                return 0
            else:
                return len(acc_mask) - 1
        else:
            correct_idx = np.argwhere(acc_mask == True)[:, 0]
            if self.when_true == "prefer_weaker":
                return correct_idx[0]
            else:
                return correct_idx[-1]
