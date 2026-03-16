from typing import Any


class InMemoryTemplateRepository:
    def __init__(self) -> None:
        self._profiles: list[dict[str, Any]] = []

    def add(self, profile: dict[str, Any]) -> None:
        self._profiles.append(profile)

    def list_all(self) -> list[dict[str, Any]]:
        return list(self._profiles)

    def clear(self) -> None:
        self._profiles.clear()