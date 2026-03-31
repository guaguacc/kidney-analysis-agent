import json
from typing import Any, Dict


KIDNEY_ANALYSIS_SYSTEM_PROMPT = """
你是一个肾病相关指标分析助手。

你的任务：
1. 只根据提供的患者指标数据和规则分析结果进行解释；
2. 不要做明确诊断；
3. 不要夸大结论；
4. 使用专业、谨慎、清晰的中文；
5. 必须只返回 JSON，不要返回 markdown，不要加代码块。

返回格式必须为：
{
  "summary": "总体结论，中文",
  "explanation": "对异常指标及其意义的解释，中文",
  "recommendations": ["建议1", "建议2"],
  "caution": "风险提示，强调这不是诊断，需要结合医生意见"
}
""".strip()


def build_kidney_analysis_prompt(
    patient_data: Dict[str, Any],
    rule_result: Dict[str, Any]
) -> str:
    patient_json = json.dumps(patient_data, ensure_ascii=False, indent=2)
    rule_json = json.dumps(rule_result, ensure_ascii=False, indent=2)

    return f"""
患者结构化数据：
{patient_json}

规则分析结果：
{rule_json}

请基于以上内容生成中文分析结果。
要求：
1. 只能输出 JSON；
2. 所有字段内容必须是中文；
3. recommendations 必须是中文列表；
4. 不要输出任何 JSON 之外的解释。
""".strip()