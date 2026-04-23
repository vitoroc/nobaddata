from typing import List

from nobaddata.models.result import CheckResult


class Reporter:
    def __init__(self, show_details: bool = False):
        self.show_details = show_details

    def render(self, results: List[CheckResult]) -> str:
        lines = []

        for r in results:
            icon = self._get_icon(r.status)

            line = f"{icon} {r.check_name} -> {r.status}"

            if self.show_details and r.details:
                line += f" | {self._format_details(r.details)}"

            lines.append(line)

        return "\n".join(lines)

    def _get_icon(self, status: str) -> str:
        if status == "PASS":
            return "✔"
        if status == "FAIL":
            return "✖"
        return "⚠"

    def _format_details(self, details: dict) -> str:
        return ", ".join(f"{k}={v}" for k, v in details.items())
