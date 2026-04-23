import pandas as pd
import pytest

from nobaddata.checks.range import RangeCheck


class BrokenDF:
    def __init__(self):
        self.columns = ["age"]

    def __len__(self):
        raise Exception("forced error")

    def __getitem__(self, key):
        raise Exception("forced error")


def test_range_check_pass_within_bounds():
    df = pd.DataFrame({"age": [10, 20, 30]})
    check = RangeCheck(column="age", min_value=0, max_value=100)

    result = check.run(df)

    assert result.status == "PASS"
    assert result.details["out_of_range_count"] == 0


def test_range_check_fail_out_of_range():
    df = pd.DataFrame({"age": [10, 20, 150]})
    check = RangeCheck(column="age", min_value=0, max_value=100)

    result = check.run(df)

    assert result.status == "FAIL"
    assert result.details["out_of_range_count"] == 1


def test_range_check_min_only():
    df = pd.DataFrame({"age": [5, 10, 20]})
    check = RangeCheck(column="age", min_value=10)

    result = check.run(df)

    assert result.status == "FAIL"
    assert result.details["out_of_range_count"] == 1


def test_range_check_max_only():
    df = pd.DataFrame({"age": [5, 10, 20]})
    check = RangeCheck(column="age", max_value=15)

    result = check.run(df)

    assert result.status == "FAIL"
    assert result.details["out_of_range_count"] == 1


def test_range_check_empty_dataframe():
    df = pd.DataFrame({"age": []})
    check = RangeCheck(column="age", min_value=0, max_value=100)

    result = check.run(df)

    assert result.status == "PASS"
    assert result.details["out_of_range_count"] == 0


def test_range_check_column_not_found():
    df = pd.DataFrame({"name": ["a", "b"]})
    check = RangeCheck(column="age", min_value=0, max_value=100)

    result = check.run(df)

    assert result.status == "ERROR"
    assert "not found" in result.details["error"]


def test_range_check_boundary_values():
    df = pd.DataFrame({"age": [0, 100]})
    check = RangeCheck(column="age", min_value=0, max_value=100)

    result = check.run(df)

    assert result.status == "PASS"


def test_range_check_requires_at_least_one_bound():
    with pytest.raises(ValueError):
        RangeCheck(column="age")


def test_range_check_forced_error():
    df = BrokenDF()
    check = RangeCheck(column="age", min_value=0, max_value=100)

    result = check.run(df)

    assert result.status == "ERROR"
    assert "forced error" in result.details["error"]
