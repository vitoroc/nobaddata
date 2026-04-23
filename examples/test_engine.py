import pandas as pd

from nobaddata.core.check import Check
from nobaddata.core.engine import Engine
from nobaddata.models.result import CheckResult


class DummyCheck(Check):
    def run(self, df: pd.DataFrame) -> CheckResult:
        return CheckResult(
            check_name=self.name,
            status="PASS",
            severity=self.severity,
            details={"rows": len(df)},
        )


class BrokenCheck(Check):
    def run(self, df):
        raise ValueError("Something went wrong")


df = pd.DataFrame({"a": [1, 2, 3]})

checks = [
    DummyCheck(name="dummy_1"),
    BrokenCheck(name="broken_1"),
]

engine = Engine(checks)

results = engine.run(df)

for r in results:
    print(r)
