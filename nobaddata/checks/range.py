from nobaddata.core.check import Check
from nobaddata.models.result import CheckResult


class RangeCheck(Check):
    def __init__(
        self,
        column: str,
        min_value: float = None,
        max_value: float = None,
        severity: str = "WARNING",
    ):
        if min_value is None and max_value is None:
            raise ValueError("At least one of min_value or max_value must be provided")

        self.column = column
        self.min_value = min_value
        self.max_value = max_value

        name_parts = [f"range_check_{column}"]
        if min_value is not None:
            name_parts.append(f"min_{min_value}")
        if max_value is not None:
            name_parts.append(f"max_{max_value}")

        super().__init__(name="_".join(name_parts), severity=severity)

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
                        "out_of_range_count": 0,
                        "total_rows": 0,
                        "min_value": self.min_value,
                        "max_value": self.max_value,
                    },
                )

            series = df[self.column]

            mask = True

            if self.min_value is not None:
                mask &= series >= self.min_value

            if self.max_value is not None:
                mask &= series <= self.max_value

            out_of_range = ~mask
            out_of_range_count = int(out_of_range.sum())

            ratio = out_of_range_count / total_rows

            status = "FAIL" if ratio > 0 else "PASS"

            return CheckResult(
                check_name=self.name,
                status=status,
                severity=self.severity,
                details={
                    "column": self.column,
                    "out_of_range_count": out_of_range_count,
                    "total_rows": int(total_rows),
                    "out_of_range_ratio": float(ratio),
                    "min_value": self.min_value,
                    "max_value": self.max_value,
                },
            )

        except Exception as e:
            return CheckResult(
                check_name=self.name,
                status="ERROR",
                severity=self.severity,
                details={"error": str(e)},
            )
