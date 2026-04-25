from typing import List

from nobaddata.models.result import CheckResult


class ConsoleReporter:
    STATUS_ICONS = {
        "PASS": "✅",
        "FAIL": "❌",
        "ERROR": "⚠️",
    }

    def report(self, results: List[CheckResult], fail_only: bool = False) -> None:
        print("\n🔍 Running Data Quality Checks...\n")

        filtered_results = self._filter_results(results, fail_only)

        if fail_only and not filtered_results:
            print("✅ All checks passed!")

        for r in filtered_results:
            icon = self.STATUS_ICONS.get(r.status, "")
            details_str = self._format_details(r.details)

            print(
                f"{icon} {r.check_name:<25} [{r.status}]"
                + (f"  {details_str}" if details_str else "")
            )

        self._print_summary(results)

    def _format_details(self, details: dict) -> str:
        if not details:
            return ""

        # temp to avoid visual polution
        items = list(details.items())[:2]

        return ", ".join(f"{k}={v}" for k, v in items)

    def _print_summary(self, results: List[CheckResult]) -> None:
        total = len(results)
        counts = {"PASS": 0, "FAIL": 0, "ERROR": 0}

        for r in results:
            counts[r.status] += 1

        print("\n" + "─" * 34)
        print("Summary:")
        print(f"Total: {total}")
        print(f"PASS: {counts['PASS']}")
        print(f"FAIL: {counts['FAIL']}")
        print(f"ERROR: {counts['ERROR']}")

    def _filter_results(self, results: List[CheckResult], fail_only: bool):
        if not fail_only:
            return results

        return [r for r in results if r.status in ("FAIL", "ERROR")]
