from logging import config
from typing import List

import yaml

from nobaddata.core.check import Check
from nobaddata.core.registry import CHECK_REGISTRY


def load_checks_from_yaml(path: str) -> List[Check]:
    with open(path, "r") as f:
        config = yaml.safe_load(f)  # safe_load to avoid dangerous objects from yaml
    checks = []

    for check_conf in config.get("checks", []):
        check_type = check_conf.pop("type")

        if check_type not in CHECK_REGISTRY:
            raise ValueError(f"Unknown check type: {check_type}")

        check_class = CHECK_REGISTRY[check_type]

        check = check_class(**check_conf)
        checks.append(check)

    return checks
