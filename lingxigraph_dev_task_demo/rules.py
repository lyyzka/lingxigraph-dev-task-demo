"""Deterministic text-processing rules for the demo."""

from __future__ import annotations

import re


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


def normalize_whitespace(text: str) -> str:
    """Trim leading/trailing whitespace and collapse repeated whitespace."""

    return re.sub(r"\s+", " ", text).strip()


def extract_keywords(text: str) -> list[str]:
    """Extract deterministic keywords from a normalized request."""

    keyword_groups = [
        "Python",
        "接口",
        "500",
        "报错",
        "异常",
        "失败",
        "实现",
        "开发",
        "创建",
        "添加",
        "解释",
        "原理",
        "区别",
        "为什么",
        "部署",
        "删除",
        "重启",
        "迁移",
        "推送",
    ]

    return [keyword for keyword in keyword_groups if keyword.lower() in text.lower()]


def build_task_structure(text: str) -> tuple[str, list[str]]:
    """Return a deterministic analysis summary and plan steps."""

    keywords = extract_keywords(text)

    debug_markers = ("500", "报错", "异常", "失败", "无法运行", "错误")
    implement_markers = ("实现", "开发", "创建", "添加")
    explain_markers = ("解释", "原理", "区别", "为什么")
    operate_markers = ("部署", "删除", "重启", "迁移", "推送")

    if any(marker in text for marker in debug_markers):
        category = "故障排查"
        plan_steps = DEBUG_PLAN_STEPS
    elif any(marker in text for marker in implement_markers):
        category = "功能实现"
        plan_steps = IMPLEMENT_PLAN_STEPS
    elif any(marker in text for marker in explain_markers):
        category = "概念解释"
        plan_steps = EXPLAIN_PLAN_STEPS
    elif any(marker in text for marker in operate_markers):
        category = "环境操作"
        plan_steps = OPERATE_PLAN_STEPS
    else:
        category = "通用开发任务"
        plan_steps = DEFAULT_PLAN_STEPS

    keyword_text = "、".join(keywords) if keywords else "未发现明显关键词"
    analysis = f"任务初步识别为{category}，提取到的关键词：{keyword_text}。"

    # Return a copy so callers cannot mutate the module-level constant.
    return analysis, list(plan_steps)
