"""Deterministic text-processing and routing rules for the demo."""

from __future__ import annotations

import re

from lingxigraph_dev_task_demo.state import TaskType


DEFAULT_PLAN_STEPS = [
    "明确任务目标",
    "收集必要上下文",
    "拆分处理步骤",
    "验证处理结果",
]

DEBUG_PLAN_STEPS = [
    "检查异常日志",
    "定位接口入口",
    "检查依赖调用",
    "构造最小复现",
]

IMPLEMENT_PLAN_STEPS = [
    "明确功能需求",
    "定位需要修改的模块",
    "设计实现方案",
    "编写并运行测试",
]

EXPLAIN_PLAN_STEPS = [
    "识别核心概念",
    "说明工作原理",
    "给出关键示例",
    "总结适用场景",
]

OPERATE_PLAN_STEPS = [
    "确认目标环境",
    "检查当前运行状态",
    "制定操作步骤",
    "验证操作结果",
]


TASK_TYPE_MARKERS: dict[TaskType, tuple[str, ...]] = {
    "operate": (
        "部署",
        "删除",
        "重启",
        "迁移",
        "推送",
        "发布",
        "回滚",
    ),
    "debug": (
        "500",
        "报错",
        "异常",
        "失败",
        "无法运行",
        "错误",
        "超时",
        "修复",
        "排查",
    ),
    "implement": (
        "实现",
        "开发",
        "创建",
        "添加",
        "编写",
        "新增",
    ),
    "explain": (
        "解释",
        "原理",
        "区别",
        "为什么",
        "介绍",
        "说明",
    ),
    "unknown": (),
}


# 当一个请求同时包含多类关键词时，按此固定顺序选择。
#
# operate 放在最前面，是一种保守路由策略：
# 带有部署、删除或重启等操作意图的请求，不应因为同时出现
# “失败”或“为什么”等词而被其他类别覆盖。
ROUTE_PRIORITY: tuple[TaskType, ...] = (
    "operate",
    "debug",
    "implement",
    "explain",
)


def normalize_whitespace(text: str) -> str:
    """Trim leading/trailing whitespace and collapse repeated whitespace."""

    return re.sub(r"\s+", " ", text).strip()


def classify_task_type(text: str) -> TaskType:
    """Classify a request using deterministic keyword rules.

    The function has no randomness, external model calls, time dependency,
    or mutable global state. The same text therefore always produces the
    same task type.
    """

    candidate = normalize_whitespace(text).lower()

    for task_type in ROUTE_PRIORITY:
        markers = TASK_TYPE_MARKERS[task_type]
        if any(marker.lower() in candidate for marker in markers):
            return task_type

    return "unknown"


def extract_keywords(text: str) -> list[str]:
    """Extract deterministic keywords from a normalized request."""

    keyword_groups = [
        "Python",
        "接口",
        "500",
        "报错",
        "异常",
        "失败",
        "错误",
        "超时",
        "修复",
        "排查",
        "实现",
        "开发",
        "创建",
        "添加",
        "编写",
        "新增",
        "解释",
        "原理",
        "区别",
        "为什么",
        "介绍",
        "说明",
        "部署",
        "删除",
        "重启",
        "迁移",
        "推送",
        "发布",
        "回滚",
    ]

    lowered_text = text.lower()

    return [
        keyword
        for keyword in keyword_groups
        if keyword.lower() in lowered_text
    ]


def build_task_structure(text: str) -> tuple[str, list[str]]:
    """Return a deterministic Stage 1 analysis summary and plan steps."""

    keywords = extract_keywords(text)
    task_type = classify_task_type(text)

    if task_type == "debug":
        category = "故障排查"
        plan_steps = DEBUG_PLAN_STEPS
    elif task_type == "implement":
        category = "功能实现"
        plan_steps = IMPLEMENT_PLAN_STEPS
    elif task_type == "explain":
        category = "概念解释"
        plan_steps = EXPLAIN_PLAN_STEPS
    elif task_type == "operate":
        category = "环境操作"
        plan_steps = OPERATE_PLAN_STEPS
    else:
        category = "通用开发任务"
        plan_steps = DEFAULT_PLAN_STEPS

    keyword_text = "、".join(keywords) if keywords else "未发现明显关键词"
    analysis = f"任务初步识别为{category}，提取到的关键词：{keyword_text}。"

    # Return a copy so callers cannot mutate the module-level constant.
    return analysis, list(plan_steps)
