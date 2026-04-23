from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class CheckResult:
    check_name: str
    status: str  # "PASS", "FAIL", "ERROR"
    severity: str  # "INFO", "WARNING", "CRITICAL"
    details: Dict[str, Any]
