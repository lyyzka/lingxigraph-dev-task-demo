"""The lingxigraph-dev-task-demo agent graph.

This module is imported by the LingxiGraph Worker from ``lingxigraph.json``.
Only code shipped with the image is trusted; nothing is uploaded at runtime.
"""

from __future__ import annotations

from typing import TypedDict

from lingxigraph import END, START, Runtime, StateGraph


class State(TypedDict):
    request: str
    result: str


class Context(TypedDict, total=False):
    tenant: str


def respond(state: State, runtime: Runtime[Context]) -> dict[str, str]:
    tenant = (runtime.context or {}).get("tenant", "local")
    runtime.emit("progress", {"stage": "respond", "tenant": tenant})
    return {"result": f"[{tenant}] handled: {state['request']}"}


builder = StateGraph(State, context_schema=Context, name="lingxigraph_dev_task_demo", version="1.0.0")
builder.add_node("respond", respond, timeout=30)
builder.add_edge(START, "respond")
builder.add_edge("respond", END)

graph = builder.compile()
