from nobaddata.core.check import Check
from nobaddata.core.registry import register_check
from nobaddata.models.result import CheckResult


@register_check("null_check")
class NullCheck(Check):
    def __init__(self, column: str, threshold: float = 0.0, severity: str = "WARNING"):
        if not 0 <= threshold <= 1:
            raise ValueError("Threshold must be between 0 and 1")

        super().__init__(name=f"null_check_{column}", severity=severity)
        self.column = column
        self.threshold = threshold

    def run(self, df):
        try:
            if self.column not in df.columns:
                return CheckResult(
                    check_name=self.name,
                    status="ERROR",
                    severity=self.severity,
                    details={"error": f"Column '{self.column}' not found"},
                )

            total_rows = len(df)

            if total_rows == 0:
                return CheckResult(
                    check_name=self.name,
                    status="PASS",
                    severity=self.severity,
                    details={
                        "column": self.column,
                        "null_count": 0,
                        "total_rows": 0,
                        "null_ratio": 0.0,
                        "threshold": self.threshold,
                    },
                )

            null_count = df[self.column].isna().sum()
            null_ratio = null_count / total_rows

            status = "FAIL" if null_ratio > self.threshold else "PASS"

            return CheckResult(
                check_name=self.name,
                status=status,
                severity=self.severity,
                details={
                    "column": self.column,
                    "null_count": int(null_count),
                    "total_rows": int(total_rows),
                    "null_ratio": float(null_ratio),
                    "threshold": self.threshold,
                },
            )

        except Exception as e:
            return CheckResult(
                check_name=self.name,
                status="ERROR",
                severity=self.severity,
                details={"error": str(e)},
            )
