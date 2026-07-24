"""Stage 2: deterministic conditional routing."""

from __future__ import annotations

from typing import TypedDict

from lingxigraph import END, START, Runtime, StateGraph

from lingxigraph_dev_task_demo.rules import (
    DEBUG_PLAN_STEPS,
    DEFAULT_PLAN_STEPS,
    EXPLAIN_PLAN_STEPS,
    IMPLEMENT_PLAN_STEPS,
    OPERATE_PLAN_STEPS,
    classify_task_type,
    normalize_whitespace,
)
from lingxigraph_dev_task_demo.state import DeveloperTaskState, TaskType


class Stage2Context(TypedDict, total=False):
    """Optional runtime context for Stage 2."""

    source: str


def normalize_request(
    state: DeveloperTaskState,
    runtime: Runtime[Stage2Context],
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


def classify_task(
    state: DeveloperTaskState,
    runtime: Runtime[Stage2Context],
) -> dict[str, TaskType]:
    """Classify the normalized request using deterministic rules."""

    task_type = classify_task_type(state["normalized_request"])

    runtime.stream_writer(
        {
            "stage": "classify_task",
            "message": "任务类型分类已完成",
            "task_type": task_type,
        }
    )

    return {
        "task_type": task_type,
    }


def route_task(state: DeveloperTaskState) -> TaskType:
    """Return the route selected by the classification node."""

    return state.get("task_type", "unknown")


def explain_task(
    state: DeveloperTaskState,
    runtime: Runtime[Stage2Context],
) -> dict[str, str | list[str]]:
    """Generate guidance for a concept-explanation request."""

    analysis = (
        "该请求属于概念解释任务。建议先界定核心概念，"
        "再说明运行原理，并通过示例建立直观理解。"
    )
    plan_steps = list(EXPLAIN_PLAN_STEPS)

    runtime.stream_writer(
        {
            "stage": "explain_task",
            "message": "已生成概念解释方案",
            "task_type": state["task_type"],
        }
    )

    return {
        "analysis": analysis,
        "plan_steps": plan_steps,
    }


def implement_task(
    state: DeveloperTaskState,
    runtime: Runtime[Stage2Context],
) -> dict[str, str | list[str]]:
    """Generate guidance for a feature-implementation request."""

    analysis = (
        "该请求属于功能实现任务。建议先明确输入输出与验收条件，"
        "再定位模块、设计改动并通过测试验证。"
    )
    plan_steps = list(IMPLEMENT_PLAN_STEPS)

    runtime.stream_writer(
        {
            "stage": "implement_task",
            "message": "已生成功能实现方案",
            "task_type": state["task_type"],
        }
    )

    return {
        "analysis": analysis,
        "plan_steps": plan_steps,
    }


def debug_task(
    state: DeveloperTaskState,
    runtime: Runtime[Stage2Context],
) -> dict[str, str | list[str]]:
    """Generate guidance for a debugging request."""

    analysis = (
        "该请求属于故障排查任务。建议从可观测证据入手，"
        "沿调用链缩小问题范围，并构造最小复现验证原因。"
    )
    plan_steps = list(DEBUG_PLAN_STEPS)

    runtime.stream_writer(
        {
            "stage": "debug_task",
            "message": "已生成故障排查方案",
            "task_type": state["task_type"],
        }
    )

    return {
        "analysis": analysis,
        "plan_steps": plan_steps,
    }


def operate_task(
    state: DeveloperTaskState,
    runtime: Runtime[Stage2Context],
) -> dict[str, str | list[str]]:
    """Generate guidance for an environment-operation request."""

    analysis = (
        "该请求属于环境操作任务。建议先确认目标环境和当前状态，"
        "再制定可验证、可回退的操作步骤。"
    )
    plan_steps = list(OPERATE_PLAN_STEPS)

    runtime.stream_writer(
        {
            "stage": "operate_task",
            "message": "已生成环境操作方案",
            "task_type": state["task_type"],
        }
    )

    return {
        "analysis": analysis,
        "plan_steps": plan_steps,
    }


def unknown_task(
    state: DeveloperTaskState,
    runtime: Runtime[Stage2Context],
) -> dict[str, str | list[str]]:
    """Provide a safe fallback for an unrecognized request."""

    analysis = (
        "当前请求未匹配到明确的开发任务类型。"
        "建议先补充目标、现象、运行环境和预期结果。"
    )
    plan_steps = list(DEFAULT_PLAN_STEPS)

    runtime.stream_writer(
        {
            "stage": "unknown_task",
            "message": "未识别任务已进入通用兜底分支",
            "task_type": state["task_type"],
        }
    )

    return {
        "analysis": analysis,
        "plan_steps": plan_steps,
    }


def finalize(
    state: DeveloperTaskState,
    runtime: Runtime[Stage2Context],
) -> dict[str, str]:
    """Create a unified result after any routing branch."""

    numbered_steps = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(state["plan_steps"], start=1)
    )

    task_type = state.get("task_type", "unknown")

    result = (
        f"规范化请求：{state['normalized_request']}\n\n"
        f"任务类型：{task_type}\n\n"
        f"分析：{state['analysis']}\n\n"
        f"建议步骤：\n{numbered_steps}"
    )

    runtime.stream_writer(
        {
            "stage": "finalize",
            "message": "Stage 2 条件路由执行完成",
            "task_type": task_type,
        }
    )

    return {
        "result": result,
    }


builder = StateGraph(
    DeveloperTaskState,
    context_schema=Stage2Context,
    name="stage2_router",
    version="0.2.0",
)

builder.add_node("normalize_request", normalize_request)
builder.add_node("classify_task", classify_task)
builder.add_node("explain_task", explain_task)
builder.add_node("implement_task", implement_task)
builder.add_node("debug_task", debug_task)
builder.add_node("operate_task", operate_task)
builder.add_node("unknown_task", unknown_task)
builder.add_node("finalize", finalize)

builder.add_edge(START, "normalize_request")
builder.add_edge("normalize_request", "classify_task")

builder.add_conditional_edges(
    "classify_task",
    route_task,
    {
        "explain": "explain_task",
        "implement": "implement_task",
        "debug": "debug_task",
        "operate": "operate_task",
        "unknown": "unknown_task",
    },
)

for branch_node in (
    "explain_task",
    "implement_task",
    "debug_task",
    "operate_task",
    "unknown_task",
):
    builder.add_edge(branch_node, "finalize")

builder.add_edge("finalize", END)

graph = builder.compile()
