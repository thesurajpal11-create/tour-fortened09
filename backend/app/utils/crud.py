from typing import Any


def apply_updates(instance: Any, updates: dict[str, Any]) -> Any:
    for field, value in updates.items():
        if value is not None:
            setattr(instance, field, value)
    return instance
