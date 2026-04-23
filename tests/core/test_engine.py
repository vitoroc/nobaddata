import pandas as pd

from nobaddata.core.check import Check
from nobaddata.core.engine import Engine
from nobaddata.models.result import CheckResult


class DummyCheck(Check):
    def run(self, df):
        return CheckResult(
            check_name=self.name, status="PASS", severity=self.severity, details={}
        )


class FailingCheck(Check):
    def run(self, df):
        raise ValueError("boom")


class CaptureCheck(Check):
    def run(self, df):
        return CheckResult(
            check_name=self.name,
            status="PASS",
            severity=self.severity,
            details={"rows": len(df)},
        )


def test_engine_handles_exceptions():
    df = pd.DataFrame({"a": [1]})

    checks = [
        DummyCheck("ok_check"),
        FailingCheck("bad_check"),
    ]

    engine = Engine(checks)
    results = engine.run(df)

    assert len(results) == 2

    assert results[0].status == "PASS"
    assert results[1].status == "ERROR"
    assert "boom" in results[1].details["error"]


def test_engine_preserves_order():
    df = pd.DataFrame({"a": [1]})

    checks = [
        DummyCheck("first"),
        DummyCheck("second"),
    ]

    engine = Engine(checks)
    results = engine.run(df)

    assert results[0].check_name == "first"
    assert results[1].check_name == "second"


def test_engine_with_no_checks():
    df = pd.DataFrame({"a": [1]})

    engine = Engine([])
    results = engine.run(df)

    assert results == []


def test_engine_passes_dataframe():
    df = pd.DataFrame({"a": [1, 2, 3]})

    checks = [CaptureCheck("capture")]

    engine = Engine(checks)
    results = engine.run(df)

    assert results[0].details["rows"] == 3


def test_engine_runs_all_checks():
    df = pd.DataFrame({"a": [1, 2, 3]})

    checks = [
        DummyCheck("check_1"),
        DummyCheck("check_2"),
    ]

    engine = Engine(checks)
    results = engine.run(df)

    assert len(results) == 2
    assert all(r.status == "PASS" for r in results)
