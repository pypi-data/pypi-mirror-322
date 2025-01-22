import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Callable

import anomed_utils as utils
import falcon
import numpy as np
import requests

from . import anonymizer


class InferenceResource:
    """This resource is intended for fitting estimator following the supervised
    learning paradigm.
    """

    def __init__(
        self,
        anonymizer_identifier: str,
        model_filepath: str | Path,
        model_loader: Callable[[str | Path], anonymizer.SupervisedLearningAnonymizer],
        default_batch_size: int,
        tuning_data_url: str,
        validation_data_url: str,
        utility_evaluation_url: str,
    ) -> None:
        self._anon_id = anonymizer_identifier
        self._model_filepath = Path(model_filepath)
        self._load_model = model_loader
        self._default_batch_size = default_batch_size
        self._url_mapper = dict(
            tuning=tuning_data_url,
            validation=validation_data_url,
            utility=utility_evaluation_url,
        )
        self._timeout = 10.0
        self._loaded_model: anonymizer.SupervisedLearningAnonymizer = None  # type: ignore
        self._loaded_model_modification_time: datetime = None  # type: ignore
        self._expected_array_label = "X"

    def on_post_predict(self, req: falcon.Request, resp: falcon.Response) -> None:
        self._load_most_recent_model()

        array_bytes = req.bounded_stream.read()
        array = utils.bytes_to_named_ndarrays_or_raise(
            array_bytes,
            expected_array_labels=[self._expected_array_label],
            error_status=falcon.HTTP_BAD_REQUEST,
            error_message="Supplied array is not compatible with the anonymizer.",
        )
        X = array[self._expected_array_label]
        validate_anonymizer_input_or_raise(
            X,
            self._loaded_model,
            error_status=falcon.HTTP_BAD_REQUEST,
            error_message="Supplied array is not compatible with the anonymizer.",
        )

        batch_size = req.get_param_as_int("batch_size", default=None)
        prediction = self._loaded_model.predict(X=X, batch_size=batch_size)
        resp.data = utils.named_ndarrays_to_bytes(dict(prediction=prediction))
        resp.status = falcon.HTTP_CREATED

    def on_post_evaluate(self, req: falcon.Request, resp: falcon.Response) -> None:
        self._load_most_recent_model()
        data_split = req.get_param("data_split", required=True)
        if data_split not in self._url_mapper.keys():
            raise falcon.HTTPBadRequest(
                description=f"Invalid value for parameter 'data_split': {data_split}. "
                "It needs to be 'tuning', or 'validation'."
            )
        array = utils.get_named_arrays_or_raise(
            data_url=self._url_mapper[data_split],
            expected_array_labels=[self._expected_array_label],
            timeout=self._timeout,
        )

        X = array[self._expected_array_label]
        prediction = self._loaded_model.predict(X, self._default_batch_size)

        try:
            evaluation_response = requests.post(
                url=self._url_mapper["utility"],
                data=utils.named_ndarrays_to_bytes(dict(prediction=prediction)),
                params=dict(anonymizer=self._anon_id, data_split=data_split),
                timeout=self._timeout,
            )
            if evaluation_response.status_code != 201:
                raise ValueError
            resp.text = json.dumps(
                dict(
                    message=(
                        f"The anonymizer has been evaluated based on {data_split} data."
                    ),
                    evaluation=evaluation_response.json(),
                )
            )
            resp.status = falcon.HTTP_CREATED
        except ValueError:
            raise falcon.HTTPInternalServerError(
                description="Utility evaluation failed."
            )
        except requests.Timeout:
            raise falcon.HTTPServiceUnavailable(
                description="Challenge currently not available for evaluation."
            )

    def _load_most_recent_model(self) -> None:
        if not self._model_filepath.exists():
            error_msg = "This anonymizer is not fitted/trained yet."
            logging.exception(error_msg)
            raise falcon.HTTPBadRequest(
                description=error_msg,
            )
        mod_time_from_disk = datetime.fromtimestamp(
            self._model_filepath.stat().st_mtime
        )
        if _is_older(self._loaded_model_modification_time, mod_time_from_disk):
            self._loaded_model = self._load_model(self._model_filepath)
            self._loaded_model_modification_time = mod_time_from_disk
        else:
            # keep the current model as it is already recent enough
            pass


def _is_older(dt1: datetime | None, dt2: datetime) -> bool:
    """Tell whether `dt1` is older (i.e. more in the past) than `dt2`. If `dt1`
    is the same as `dt2`, or even if `dt1` is `None`, output `True`."""
    if dt1 is None:
        return True
    else:
        return dt1 <= dt2


def supervised_learning_anonymizer_server_factory(
    anonymizer_identifier: str,
    anonymizer_obj: anonymizer.SupervisedLearningAnonymizer,
    model_filepath: str | Path,
    default_batch_size: int,
    training_data_url: str,
    tuning_data_url: str,
    validation_data_url: str,
    utility_evaluation_url: str,
    model_loader: Callable[[str | Path], anonymizer.SupervisedLearningAnonymizer],
) -> falcon.App:
    """A factory to create a web application object which hosts an
    `anonymizer.SupervisedLearningAnonymizer`, currently the most basic use
    case of anonymizers (privacy preserving ML models) for the AnoMed
    competition platform.

    By using this factory, you don't have to worry any web-programming issues,
    as they are hidden from you. The generated web app will feature the
    following routes (more details may be found in this project's openapi
    specification):

    * [GET] `/`
    * [POST] `/fit`
    * [POST] `/evaluate`
    * [POST] `/predict`

    Parameters
    ----------
    anonymizer_obj : anonymizer.SupervisedLearningAnonymizer
        An anonymizer that is based on the supervised learning paradigm

    Returns
    -------
    falcon.App
        A web application object based on the falcon web framework.
    """
    app = falcon.App()

    app.add_route(
        "/", utils.StaticJSONResource(dict(message="Anonymizer server is alive!"))
    )
    app.add_route(
        "/fit",
        utils.FitResource(
            data_getter=_get_anonymizer_fit_data(
                anonymizer=anonymizer_obj,
                training_data_url=training_data_url,
                timeout=10.0,
            ),
            model=anonymizer_obj,
            model_filepath=model_filepath,
        ),
    )
    ir = InferenceResource(
        anonymizer_identifier=anonymizer_identifier,
        model_filepath=model_filepath,
        model_loader=model_loader,
        default_batch_size=default_batch_size,
        tuning_data_url=tuning_data_url,
        validation_data_url=validation_data_url,
        utility_evaluation_url=utility_evaluation_url,
    )
    app.add_route("/evaluate", ir, suffix="evaluate")
    app.add_route("/predict", ir, suffix="predict")
    return app


def validate_anonymizer_input_or_raise(
    feature_array: np.ndarray,
    anonymizer: anonymizer.SupervisedLearningAnonymizer,
    error_status: str | int | None = falcon.HTTP_INTERNAL_SERVER_ERROR,
    error_message: str | None = None,
) -> None:
    """Validate the input for an anonymizer. If validation fails, raise a
    `falcon.HTTPError` instead.

    Parameters
    ----------
    feature_array : np.ndarray
        A NumPy array containing the features for this anonymizer.
    anonymizer : anonymizer.SupervisedLearningAnonymizer
        The anonymizer to validate input for. This function will use the
        anonymizer's `validate_input` method.
    error_status : str | int | None, optional
        The error status to use if validation fails. By default,
        `falcon.HTTP_INTERNAL_SERVER_ERROR`.
    error_message : str | None, optional
        The error message to output. By default `None`, which will result in a
        generic message derived from the `error_status`.

    Raises
    ------
    falcon.HTTPError
        If validation fails.
    """
    try:
        anonymizer.validate_input(feature_array)
    except ValueError:
        if error_status is None:
            error_status = falcon.HTTP_INTERNAL_SERVER_ERROR
        raise falcon.HTTPError(status=error_status, description=error_message)


def _get_anonymizer_fit_data(
    anonymizer: anonymizer.SupervisedLearningAnonymizer,
    training_data_url: str,
    timeout: float,
    expected_array_labels: list[str] | None = None,
) -> Callable[[], dict[str, np.ndarray]]:
    if expected_array_labels is None:
        expected_array_labels = ["X", "y"]

    def getter():
        training_data = utils.get_named_arrays_or_raise(
            data_url=training_data_url,
            expected_array_labels=expected_array_labels,
            timeout=timeout,
        )

        validate_anonymizer_input_or_raise(
            training_data[expected_array_labels[0]],
            anonymizer,
            falcon.HTTP_INTERNAL_SERVER_ERROR,
            "The anonymizer is not compatible with the training data.",
        )
        return training_data

    return getter
