import inspect
import pickle
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable

import numpy as np


class SupervisedLearningAnonymizer(ABC):
    """A base class for anonymizers (privacy preserving machine learning models)
    that rely on the supervised learning paradigm.

    Subclasses need to define a way to ...

    * fit/train the model they represent using only a feature array and a target
      array (i.e. without explicitly given hyperparameters)
    * use the (trained) model for inference
    * save the (trained) model to disk
    * validate model input arrays
    """

    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """Perform a full training cycle (all epochs, not just one) using the
        given features and targets.

        Parameters
        ----------
        X : np.ndarray
            The feature array.
        y : np.ndarray
            The target array.
        """
        pass

    @abstractmethod
    def predict(self, X: np.ndarray, batch_size: int | None = None) -> np.ndarray:
        """Infer the target values of a feature array.

        Parameters
        ----------
        X : np.ndarray
            The features to infer the target values for.
        batch_size : int | None, optional
            The batch size to use while inferring (to limit compute resource
            consumption). By default `None`, which results in processing the
            whole array `X` at once.

        Returns
        -------
        np.ndarray
            The target values.
        """
        pass

    @abstractmethod
    def save(self, filepath: str | Path) -> None:
        """Save the instance to disk, maintaining the current training progress.

        Parameters
        ----------
        filepath : str | Path
            Where to save the instance.
        """
        pass

    @abstractmethod
    def validate_input(self, input_array: np.ndarray) -> None:
        """Check whether the input array is a valid argument for `fit` and for
        `predict (parameter `X`).

        If so, do nothing. Otherwise, raise a `ValueError`.

        Parameters
        ----------
        input_array : np.ndarray
            The array to validate.

        Raises
        ------
        ValueError
            If `input_array` is incompatible with this anonymizer.
        """
        pass


class WrappedAnonymizer(SupervisedLearningAnonymizer):
    """If you already have an anonymizer object that offers a `fit(X, y)` method
    and either a `predict(X)` or `predict(X, batch_size)` too, use this wrapper
    to lift it to a `SupervisedLearningAnonymizer`. If your object also features
    `save`, it will used. Otherwise, provide a replacement functions at
    initialization."""

    def __init__(
        self,
        anonymizer,
        serializer: Callable[[Any, str | Path], None] | None = None,
        input_array_validator: Callable[[np.ndarray], None] | None = None,
    ) -> None:
        """
        Parameters
        ----------
        anonymizer
            The object to be wrapped as a `SupervisedLearningAnonymizer`. It
            should implement a `fit(X: np.ndarray, y: np.ndarray)` and either a
            `predict(X: np.ndarray)` or a
            `predict(X: np.ndarray, batch_size: int | None)`.
        serializer : Callable[[Any, str | Path], None] | None, optional
            The serializer (pickler) to use, if `anonymizer` does not provide a
            `save` method. The first argument of the serializer is `anonymizer`
            and the second the filepath. By default `None`, which means
            invoking `anonymizer.save(...)`.
        input_array_validator : Callable[[np.ndarray], None] | None, optional
            The array input validator to use, if `anonymizer` does not provide
            a `validate_input` method. By default `None`, which means invoking
            `anonymizer.validate_input(...)`.

        Raises
        ------
        NotImplementedError
            If `anonymizer` does not provide a `fit` or `predict` method.
        """
        if not hasattr(anonymizer, "fit"):
            raise NotImplementedError(
                "Anonymizer object does not provide a fit function."
            )
        if not hasattr(anonymizer, "predict"):
            raise NotImplementedError(
                "Anonymizer object does not provide a predict function."
            )
        self._anonymizer = anonymizer

        self._serialize = serializer
        self._validate = input_array_validator

    def fit(self, X: np.ndarray, y: np.ndarray):
        self._anonymizer.fit(X, y)

    def predict(self, X: np.ndarray, batch_size: int | None = None) -> np.ndarray:
        """Uses the anonymizer's `predict` method to predict the target values
        for `X`. If that method accepts a `batch_size` parameter, this makes use
        of it. Otherwise, this methods takes care of batching.

        Parameters
        ----------
        X : np.ndarray
            The feature array.
        batch_size : int | None, optional
            The batch size to use for prediction. By default `None`, which means
            use the whole array `X` at once.

        Returns
        -------
        np.ndarray
            The inferred/predicted target values.
        """
        sig = inspect.signature(self._anonymizer.predict)
        if "batch_size" in sig.parameters:
            return self._anonymizer.predict(X, batch_size=batch_size)
        else:
            predictions = [
                self._anonymizer.predict(_X) for _X in _batch_views(X, batch_size)
            ]
            return np.concatenate(predictions)

    def save(self, filepath: str | Path):
        if hasattr(self._anonymizer, "save"):
            self._anonymizer.save(filepath)
        elif self._serialize is not None:
            self._serialize(self._anonymizer, filepath)
        else:
            raise NotImplementedError(
                "Anonymizer object does not provide a save function and a "
                "replacement is also missing."
            )

    def validate_input(self, input_array: np.ndarray) -> None:
        if hasattr(self._anonymizer, "validate_input"):
            self._anonymizer.validate_input(input_array)
        elif self._validate is not None:
            self._validate(input_array)
        else:
            raise NotImplementedError(
                "Anonymizer object does not provide a validate_input function "
                "and a replacement is also missing."
            )


def pickle_anonymizer(anonymizer: Any, filepath: str | Path) -> None:
    """A pickling-based serializer to use as a replacement in
    `WrappedAnonymizer`"""
    with open(filepath, "wb") as file:
        pickle.dump(anonymizer, file)


def unpickle_anonymizer(filepath: str | Path) -> Any:
    """An inverse to `pickle_anonymizer`, to use as `model_loader` argument for
    `anonymizer_server.supervised_learning_anonymizer_server_factory`"""
    with open(filepath, "rb") as file:
        return pickle.load(file)


def _batch_views(array: np.ndarray, batch_size: int | None) -> list[np.ndarray]:
    """Create batch views of numpy arrays for a given batch size."""
    n = len(array)
    if batch_size is None or batch_size >= n:
        return [array]
    if batch_size <= 0:
        return []
    else:
        assert 0 < batch_size < n
        indices = range(batch_size, n, batch_size)
        return np.split(array, indices)
