import pytest
import sys
import os

PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PACKAGE_ROOT)
sys.path.append(PACKAGE_ROOT)

from Loanapp.config import config
from Loanapp.processing.data_handling import load_data
from Loanapp import predict

@pytest.fixture
def single_prediction():
    print("Load dataset...")
    test_dataset = load_data(config.TEST_FILE)
    single_row = test_dataset[:1]

    try:
        result = predict.generate_predictions(single_row)
        print(f"Predicted outcome - {result}")
        return result
    except Exception as e:
        print(f"Got Exception - {e}")
        raise


def test_single_pred_not_null(single_prediction):
    print("Testing if predicted result is not null...")
    assert single_prediction is not None
    print("Test Passed : Single prediction is not none")


def test_single_pred_str_type(single_prediction):
    assert isinstance(single_prediction.get("Predictions")[0],str)


def test_single_pred_validate(single_prediction):
    assert single_prediction.get("Predictions")[0] == 'Y'


def test_empty_dataset():
    empty_dataset = []
    result = predict.generate_predictions(empty_dataset)

    assert result.get("Predictions") == []


@pytest.mark.parametrize("test_input" , [
    (10),
    (55),
    (100)
])
def test_multiple_rows(test_input):
    test_dataset = load_data(config.TEST_FILE)
    row = test_dataset[test_input:test_input+1]
    result = predict.generate_predictions(row)

    assert result is not None
    assert isinstance(result.get("Predictions")[0],str)


def test_unexpected_data_format():
    invalid_inputs = [
        "invalid string",
        12345,
        {'key':'value'}
    ]
    for invalid_input in invalid_inputs:
        try:
            predict.generate_predictions(invalid_input)
        except Exception as e:
            print(e)
