"""Classification based on custom functions (e.g., rule-based classification)."""

__all__ = ("RuleClassifier",)

import abc
import warnings

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.multiclass import unique_labels

from ..utils._legacy import _fit_context


class RuleClassifier(BaseEstimator, ClassifierMixin, metaclass=abc.ABCMeta):
    """ABC that defines rule-based inference methods."""

    def __init__(self, *, validate=False, warn_no_implemented=True, kw_args=None):
        self.validate = validate
        self.warn_no_implemented = warn_no_implemented
        self.kw_args = kw_args

        if not self.validate:
            self.is_fitted_ = True

    @_fit_context(prefer_skip_nested_validation=False)
    def fit(self, X, y, sample_weight=None):
        """Fits the estimator and sets fit attributes.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,) or (n_samples, n_outputs)
            The target values.

        Returns
        -------
        self : object
            Returns self.
        """
        classes = unique_labels(y)
        self.partial_fit(X, y, classes, sample_weight=sample_weight)
        return self

    # pylint: disable=unused-argument
    @_fit_context(prefer_skip_nested_validation=False)
    def partial_fit(self, X, y, classes=None, sample_weight=None):
        """Fits the estimator partially."""
        if self.validate:
            try:
                self.predict(X)
                self.predict_proba(X)
                self.predict_log_proba(X)
                self.decision_function(X)
            except NotImplementedError:
                if self.warn_no_implemented:
                    warnings.warn(
                        (
                            f"Some inference methods for {self.__class__.__name__} are "
                            f"not implemented"
                        ),
                        category=UserWarning,
                    )
            except Exception:
                warnings.warn(
                    (
                        "Validation of inference methods resulted in errors; "
                        "please, check your implementations",
                    ),
                    category=UserWarning,
                )
                raise

        self.classes_ = classes
        self.is_fitted_ = True

        return self

    def predict(self, X):
        """Predicts hard labels.

        Parameters
        ----------
        X : indexable, length n_samples
            Input samples to classify.
            Must fulfill the input assumptions of the
            underlying estimator.
        """
        raise NotImplementedError

    def decision_function(self, X):
        """Predicts decision scores.

        Parameters
        ----------
        X : indexable, length n_samples
            Input samples to classify.
            Must fulfill the input assumptions of the
            underlying estimator.
        """
        raise NotImplementedError

    def predict_proba(self, X):
        """Predicts probabilities.

        Parameters
        ----------
        X : indexable, length n_samples
            Input samples to classify.
            Must fulfill the input assumptions of the
            underlying estimator.
        """
        raise NotImplementedError

    def predict_log_proba(self, X):
        """Predicts log-probabilities.

        Parameters
        ----------
        X : indexable, length n_samples
            Input samples to classify.
            Must fulfill the input assumptions of the
            underlying estimator.
        """
        raise NotImplementedError

    def get_params(self, deep=True):
        """Gets parameters for the estimator."""
        parameters = super().get_params(deep)
        parameters |= {**self.kw_args}
        return parameters

    def set_params(self, **params):
        """Sets the parameters of the estimator."""
        for key, value in params.items():
            if key in {"validate", "warn_no_implemented"}:
                setattr(self, key, value)
            else:
                self.kw_args[key] = value
        return self
