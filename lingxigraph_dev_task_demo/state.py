"""State definitions for the Developer Task Assistant demo."""

from __future__ import annotations

from typing import Literal, TypedDict


TaskType = Literal[
    "explain",
    "implement",
    "debug",
    "operate",
    "unknown",
]


class DeveloperTaskInput(TypedDict):
    """Input accepted by the graph."""

    request: str


class DeveloperTaskState(DeveloperTaskInput, total=False):
    """Shared state passed between Developer Task Assistant graph nodes.

    Only JSON-serializable values are stored in the graph state.
    """

    normalized_request: str
    task_type: TaskType
    analysis: str
    plan_steps: list[str]
    result: str
