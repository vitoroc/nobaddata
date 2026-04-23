import pandas as pd
import pytest

from nobaddata.checks.duplicate import DuplicateCheck


def test_duplicate_check_pass_no_duplicates():
    df = pd.DataFrame({"user_id": [1, 2, 3]})
    check = DuplicateCheck(columns=["user_id"])

    result = check.run(df)

    assert result.status == "PASS"
    assert result.details["duplicate_count"] == 0


def test_duplicate_check_fail_with_duplicates():
    df = pd.DataFrame({"user_id": [1, 1, 2]})
    check = DuplicateCheck(columns=["user_id"], threshold=0.0)

    result = check.run(df)

    assert result.status == "FAIL"
    assert result.details["duplicate_count"] == 1


def test_duplicate_check_threshold_pass():
    df = pd.DataFrame({"user_id": [1, 1, 2, 2]})
    check = DuplicateCheck(columns=["user_id"], threshold=0.5)

    result = check.run(df)

    # duplicate_count = 2 → ratio = 0.5 → should PASS
    assert result.status == "PASS"


def test_duplicate_check_threshold_fail():
    df = pd.DataFrame({"user_id": [1, 1, 2, 2]})
    check = DuplicateCheck(columns=["user_id"], threshold=0.4)

    result = check.run(df)

    assert result.status == "FAIL"


def test_duplicate_check_empty_dataframe():
    df = pd.DataFrame({"user_id": []})
    check = DuplicateCheck(columns=["user_id"])

    result = check.run(df)

    assert result.status == "PASS"
    assert result.details["duplicate_ratio"] == 0.0


def test_duplicate_check_missing_column():
    df = pd.DataFrame({"name": ["a", "b"]})
    check = DuplicateCheck(columns=["user_id"])

    result = check.run(df)

    assert result.status == "ERROR"
    assert "Columns not found" in result.details["error"]


def test_duplicate_check_multiple_columns():
    df = pd.DataFrame({"user_id": [1, 1, 2], "email": ["a", "a", "b"]})

    check = DuplicateCheck(columns=["user_id", "email"])

    result = check.run(df)

    assert result.status == "FAIL"
    assert result.details["duplicate_count"] == 1


def test_duplicate_check_all_duplicates():
    df = pd.DataFrame({"user_id": [1, 1, 1, 1]})
    check = DuplicateCheck(columns=["user_id"])

    result = check.run(df)

    # first is unique, next 3 are duplicates
    assert result.details["duplicate_count"] == 3


def test_duplicate_check_empty_columns():
    with pytest.raises(ValueError):
        DuplicateCheck(columns=[])


def test_duplicate_check_invalid_columns_type():
    with pytest.raises(TypeError):
        DuplicateCheck(columns="user_id")


def test_duplicate_check_invalid_column_element():
    with pytest.raises(TypeError):
        DuplicateCheck(columns=["user_id", 123])


def test_duplicate_check_invalid_threshold():
    with pytest.raises(ValueError):
        DuplicateCheck(columns=["user_id"], threshold=2)


def test_duplicate_check_unexpected_error():
    check = DuplicateCheck(columns=["user_id"])

    result = check.run(None)  # força erro

    assert result.status == "ERROR"
    assert "error" in result.details
