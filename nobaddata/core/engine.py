from typing import List

import pandas as pd

from nobaddata.config.loader import load_checks_from_yaml
from nobaddata.core.check import Check
from nobaddata.models.result import CheckResult


class Engine:
    def __init__(self, checks: List[Check]):
        self.checks = checks

    @classmethod
    def from_yaml(cls, path: str):
        checks = load_checks_from_yaml(path)
        return cls(checks)

    def run(self, df: pd.DataFrame) -> List[CheckResult]:
        results: List[CheckResult] = []

        for check in self.checks:
            try:
                result = check.run(df)
                results.append(result)
            except Exception as e:
                results.append(
                    CheckResult(
                        check_name=check.name,
                        status="ERROR",
                        severity=check.severity,
                        details={"error": str(e)},
                    )
                )
        return results
