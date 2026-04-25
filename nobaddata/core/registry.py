from typing import Dict, Type

from nobaddata.core.check import Check

CHECK_REGISTRY: Dict[str, Type[Check]] = {}


def register_check(name: str):
    def decorator(cls: Type[Check]):
        CHECK_REGISTRY[name] = cls
        return cls

    return decorator
