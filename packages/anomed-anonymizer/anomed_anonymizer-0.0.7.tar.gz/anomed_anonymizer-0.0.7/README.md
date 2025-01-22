[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![pipeline status](https://git.uni-luebeck.de/its/anomed/anonymizer/badges/main/pipeline.svg?ignore_skipped=true)
![coverage](https://git.uni-luebeck.de/its/anomed/anonymizer/badges/main/coverage.svg?job=run_tests)

# Anonymizer

A library aiding to create anonymizers (privacy preserving machine learning
models) for the AnoMed competition platform.

# Usage Example

```python
import sklearn
import sklearn.linear_model

import anomed_anonymizer as anonymizer

estimator = sklearn.linear_model.LinearRegression()
example_anon = anonymizer.WrappedAnonymizer(
    anonymizer=estimator,
    serializer=anonymizer.pickle_anonymizer,
    input_array_validator=lambda _: None,
)

app = anonymizer.supervised_learning_anonymizer_server_factory(
    anonymizer_identifier="example_anonymizer",
    anonymizer_obj=example_anon,
    model_filepath="model",
    default_batch_size=64,
    training_data_url="http://example.com/train",
    tuning_data_url="http://example.com/tuning",
    validation_data_url="http://example.com/validation",
    utility_evaluation_url="http://example.com/utility",
    model_loader=anonymizer.unpickle_anonymizer,
)
```
