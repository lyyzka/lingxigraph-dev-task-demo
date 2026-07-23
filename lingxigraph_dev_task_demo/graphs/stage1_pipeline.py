"""Stage 1: deterministic text-processing pipeline."""

from __future__ import annotations

from typing import TypedDict

from lingxigraph import END, START, Runtime, StateGraph

from lingxigraph_dev_task_demo.rules import (
    build_task_structure,
    normalize_whitespace,
)
from lingxigraph_dev_task_demo.state import DeveloperTaskState


class Stage1Context(TypedDict, total=False):
    """Optional runtime context for Stage 1."""

    source: str


def normalize_request(
    state: DeveloperTaskState,
    runtime: Runtime[Stage1Context],
) -> dict[str, str]:
    """Normalize the request while preserving the original input."""

    normalized_request = normalize_whitespace(state["request"])

    runtime.stream_writer(
        {
            "stage": "normalize_request",
            "message": "用户输入已完成规范化",
            "normalized_request": normalized_request,
        }
    )

    return {
        "normalized_request": normalized_request,
    }


def structure_task(
    state: DeveloperTaskState,
    runtime: Runtime[Stage1Context],
) -> dict[str, str | list[str]]:
    """Produce deterministic analysis and plan steps."""

    normalized_request = state["normalized_request"]
    analysis, plan_steps = build_task_structure(normalized_request)

    runtime.stream_writer(
        {
            "stage": "structure_task",
            "message": "任务结构化分析已完成",
            "step_count": len(plan_steps),
        }
    )

    return {
        "analysis": analysis,
        "plan_steps": plan_steps,
    }


def finalize(
    state: DeveloperTaskState,
    runtime: Runtime[Stage1Context],
) -> dict[str, str]:
    """Create the unified human-readable result."""

    numbered_steps = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(state["plan_steps"], start=1)
    )

    result = (
        f"规范化请求：{state['normalized_request']}\n\n"
        f"分析：{state['analysis']}\n\n"
        f"建议步骤：\n{numbered_steps}"
    )

    runtime.stream_writer(
        {
            "stage": "finalize",
            "message": "Stage 1 流水线执行完成",
        }
    )

    return {
        "result": result,
    }


builder = StateGraph(
    DeveloperTaskState,
    context_schema=Stage1Context,
    name="stage1_pipeline",
    version="0.1.0",
)

builder.add_node("normalize_request", normalize_request)
builder.add_node("structure_task", structure_task)
builder.add_node("finalize", finalize)

builder.add_edge(START, "normalize_request")
builder.add_edge("normalize_request", "structure_task")
builder.add_edge("structure_task", "finalize")
builder.add_edge("finalize", END)

graph = builder.compile()
