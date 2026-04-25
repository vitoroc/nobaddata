from nobaddata.core.check import Check
from nobaddata.core.registry import register_check
from nobaddata.models.result import CheckResult


@register_check("duplicate_check")
class DuplicateCheck(Check):
    def __init__(
        self, columns: list[str], threshold: float = 0.0, severity: str = "WARNING"
    ):
        if not isinstance(columns, list):
            raise TypeError(f"Columns must be a list, got {type(columns).__name__}")
        if not columns:
            raise ValueError("At least one column must be specified")
        if not all(isinstance(col, str) for col in columns):
            raise TypeError("All elements in columns must be strings")
        if not 0 <= threshold <= 1:
            raise ValueError("Threshold must be between 0 and 1")

        unique_columns = list(dict.fromkeys(columns))
        super().__init__(
            name=f"duplicate_check_{'_'.join(unique_columns)}", severity=severity
        )
        self.columns = columns
        self.threshold = threshold

    def run(self, df):
        try:
            missing_columns = [col for col in self.columns if col not in df.columns]
            if missing_columns:
                return CheckResult(
                    check_name=self.name,
                    status="ERROR",
                    severity=self.severity,
                    details={
                        "error": f"Columns not found: {', '.join(missing_columns)}"
                    },
                )

            total_rows = len(df)

            if total_rows == 0:
                return CheckResult(
                    check_name=self.name,
                    status="PASS",
                    severity=self.severity,
                    details={
                        "columns": self.columns,
                        "duplicate_count": 0,
                        "total_rows": 0,
                        "duplicate_ratio": 0.0,
                        "threshold": self.threshold,
                    },
                )

            duplicate_count = df.duplicated(subset=self.columns).sum()
            duplicate_ratio = duplicate_count / total_rows

            status = "FAIL" if duplicate_ratio > self.threshold else "PASS"

            return CheckResult(
                check_name=self.name,
                status=status,
                severity=self.severity,
                details={
                    "columns": self.columns,
                    "duplicate_count": int(duplicate_count),
                    "total_rows": int(total_rows),
                    "duplicate_ratio": float(duplicate_ratio),
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
