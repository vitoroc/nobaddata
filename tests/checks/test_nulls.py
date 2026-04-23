import pandas as pd
import pytest

from nobaddata.checks.nulls import NullCheck


def test_null_check_pass():
    df = pd.DataFrame({"email": ["a", "b"]})
    check = NullCheck("email")

    result = check.run(df)

    assert result.status == "PASS"


def test_null_check_fail():
    df = pd.DataFrame({"email": ["a", None]})
    check = NullCheck("email")

    result = check.run(df)

    assert result.status == "FAIL"
    assert result.details["null_count"] == 1


def test_null_check_threshold():
    df = pd.DataFrame({"email": ["a", None, "b", None]})
    check = NullCheck("email", threshold=0.5)

    result = check.run(df)

    assert result.status == "PASS"


def test_null_check_column_not_found():
    df = pd.DataFrame({"name": ["a"]})
    check = NullCheck("email")

    result = check.run(df)

    assert result.status == "ERROR"


def test_null_check_empty_df():
    df = pd.DataFrame({"email": []})
    check = NullCheck("email")

    result = check.run(df)

    assert result.status == "PASS"


def test_null_check_invalid_threshold():
    with pytest.raises(ValueError):
        NullCheck("email", threshold=2)


def test_unexpected_error():
    check = NullCheck("email")

    result = check.run(None)  # df inválido

    assert result.status == "ERROR"
