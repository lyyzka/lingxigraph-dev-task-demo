"""State definitions for the Developer Task Assistant demo."""

from __future__ import annotations

from typing import TypedDict


class DeveloperTaskInput(TypedDict):
    """Input accepted by the graph."""

    request: str


class DeveloperTaskState(DeveloperTaskInput, total=False):
    """Shared state passed between Stage 1 graph nodes.

    Only JSON-serializable values are stored in the graph state.
    """

    normalized_request: str
    analysis: str
    plan_steps: list[str]
    result: str
