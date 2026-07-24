"""Tests for the Stage 2 deterministic conditional router."""

from __future__ import annotations

import pytest

from lingxigraph_dev_task_demo.graphs.stage2_router import graph
from lingxigraph_dev_task_demo.rules import classify_task_type
from lingxigraph_dev_task_demo.state import TaskType


@pytest.mark.parametrize(
    ("user_request", "expected_type", "expected_first_step"),
    [
        (
            "解释 Python 装饰器的执行过程",
            "explain",
            "识别核心概念",
        ),
        (
            "为项目添加健康检查接口",
            "implement",
            "明确功能需求",
        ),
        (
            "修复数据库连接超时问题",
            "debug",
            "检查异常日志",
        ),
        (
            "将新版本部署到生产服务器",
            "operate",
            "确认目标环境",
        ),
        (
            "帮我看看这个任务",
            "unknown",
            "明确任务目标",
        ),
    ],
)
def test_routes_request_to_expected_branch(
    user_request: str,
    expected_type: TaskType,
    expected_first_step: str,
) -> None:
    """Each representative request should reach its expected branch."""

    result = graph.invoke({"request": user_request})

    assert result["task_type"] == expected_type
    assert result["plan_steps"][0] == expected_first_step
    assert f"任务类型：{expected_type}" in result["result"]


def test_unknown_request_uses_explicit_fallback() -> None:
    """An unrecognized request should not be forced into a known category."""

    result = graph.invoke({"request": "帮我处理一下"})

    assert result["task_type"] == "unknown"
    assert "未匹配到明确的开发任务类型" in result["analysis"]
    assert "补充目标" in result["analysis"]


def test_conflicting_keywords_follow_fixed_priority() -> None:
    """Operation markers should win when several categories match."""

    request = "请解释生产环境部署失败的原因"

    results = [
        classify_task_type(request)
        for _ in range(10)
    ]

    assert results == ["operate"] * 10


def test_debug_route_executes_only_debug_branch() -> None:
    """The updates stream should contain only the selected business branch."""

    updates = list(
        graph.stream(
            {"request": "修复数据库连接超时问题"},
            stream_mode="updates",
        )
    )

    node_names = [next(iter(update)) for update in updates]

    assert node_names == [
        "normalize_request",
        "classify_task",
        "debug_task",
        "finalize",
    ]

    assert "explain_task" not in node_names
    assert "implement_task" not in node_names
    assert "operate_task" not in node_names
    assert "unknown_task" not in node_names


def test_custom_stream_reports_selected_route() -> None:
    """Custom events should expose the classification and selected branch."""

    events = list(
        graph.stream(
            {"request": "为项目创建状态检查接口"},
            stream_mode="custom",
        )
    )

    stage_names = [event["stage"] for event in events]

    assert stage_names == [
        "normalize_request",
        "classify_task",
        "implement_task",
        "finalize",
    ]

    assert events[1]["task_type"] == "implement"
    assert events[-1]["task_type"] == "implement"
