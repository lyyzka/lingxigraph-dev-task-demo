"""Tests for the Stage 1 text-processing pipeline."""

from __future__ import annotations

from lingxigraph_dev_task_demo.graphs.stage1_pipeline import graph


def test_normalizes_whitespace_and_preserves_original_request() -> None:
    request = "  请帮我   分析这个 Python 接口为什么返回 500  "

    result = graph.invoke({"request": request})

    assert result["request"] == request
    assert result["normalized_request"] == (
        "请帮我 分析这个 Python 接口为什么返回 500"
    )


def test_debug_request_generates_debug_plan() -> None:
    result = graph.invoke(
        {"request": "请分析这个 Python 接口为什么返回 500"}
    )

    assert "故障排查" in result["analysis"]
    assert result["plan_steps"] == [
        "检查异常日志",
        "定位接口入口",
        "检查依赖调用",
        "构造最小复现",
    ]
    assert "1. 检查异常日志" in result["result"]
    assert "4. 构造最小复现" in result["result"]


def test_implement_request_generates_implementation_plan() -> None:
    result = graph.invoke(
        {"request": "请为项目添加一个健康检查接口"}
    )

    assert "功能实现" in result["analysis"]
    assert result["plan_steps"] == [
        "明确功能需求",
        "定位需要修改的模块",
        "设计实现方案",
        "编写并运行测试",
    ]


def test_explain_request_generates_explanation_plan() -> None:
    result = graph.invoke(
        {"request": "请解释 Python 装饰器的执行原理"}
    )

    assert "概念解释" in result["analysis"]
    assert result["plan_steps"] == [
        "识别核心概念",
        "说明工作原理",
        "给出关键示例",
        "总结适用场景",
    ]


def test_updates_stream_contains_all_three_nodes() -> None:
    updates = list(
        graph.stream(
            {"request": "请分析接口返回 500 的原因"},
            stream_mode="updates",
        )
    )

    node_names = [next(iter(update)) for update in updates]

    assert node_names == [
        "normalize_request",
        "structure_task",
        "finalize",
    ]


def test_custom_stream_contains_all_three_stages() -> None:
    events = list(
        graph.stream(
            {"request": "请分析接口返回 500 的原因"},
            stream_mode="custom",
        )
    )

    stage_names = [event["stage"] for event in events]

    assert stage_names == [
        "normalize_request",
        "structure_task",
        "finalize",
    ]
