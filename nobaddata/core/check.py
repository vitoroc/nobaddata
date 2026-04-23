from abc import ABC, abstractmethod

import pandas as pd

from nobaddata.models.result import CheckResult


class Check(ABC):
    def __init__(self, name: str, severity: str = "WARNING"):
        self.name = name
        self.severity = severity

    @abstractmethod
    def run(self, df: pd.DataFrame) -> CheckResult:
        pass
