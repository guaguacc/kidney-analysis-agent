from typing import Any, Dict, List, Optional


class RuleEngine:
    def analyze(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        abnormal_items: List[str] = []
        recommendations: List[str] = []

        scr = patient_data.get("scr")
        egfr = patient_data.get("egfr")
        acr = patient_data.get("acr")
        sbp = patient_data.get("sbp")
        dbp = patient_data.get("dbp")
        urine_protein = patient_data.get("urine_protein")

        ckd_stage = self._get_ckd_stage(egfr)
        egfr_severity = self._get_egfr_severity(egfr)

        if scr is not None and scr > 133:
            abnormal_items.append("血肌酐升高")
            recommendations.append("建议复查血肌酐并进一步评估肾功能")

        if egfr is not None:
            if egfr < 60:
                abnormal_items.append("eGFR下降")
                recommendations.append("建议持续监测 eGFR，并评估慢性肾病风险")
            if egfr < 30:
                recommendations.append("建议尽快到肾内科进一步评估")

        if acr is not None:
            if acr >= 300:
                abnormal_items.append("尿白蛋白/肌酐比重度升高")
                recommendations.append("建议尽快复查尿白蛋白/肌酐比并评估肾损伤程度")
            elif acr >= 30:
                abnormal_items.append("尿白蛋白/肌酐比升高")
                recommendations.append("建议复查尿白蛋白/肌酐比")

        if sbp is not None and sbp >= 140:
            abnormal_items.append("收缩压升高")
            recommendations.append("建议规律监测血压")

        if dbp is not None and dbp >= 90:
            abnormal_items.append("舒张压升高")
            recommendations.append("建议规律监测血压")

        if urine_protein and str(urine_protein).lower() in {"positive", "+", "1+", "2+", "3+"}:
            abnormal_items.append("尿蛋白异常")
            recommendations.append("建议进一步做尿蛋白相关检查")

        risk_level = self._determine_risk_level(
            abnormal_items=abnormal_items,
            egfr=egfr,
            acr=acr,
        )

        summary = self._build_summary(
            abnormal_items=abnormal_items,
            ckd_stage=ckd_stage,
            egfr_severity=egfr_severity,
            risk_level=risk_level,
        )

        return {
            "risk_level": risk_level,
            "ckd_stage": ckd_stage,
            "egfr_severity": egfr_severity,
            "abnormal_items": abnormal_items,
            "rule_based_summary": summary,
            "recommendations": list(dict.fromkeys(recommendations)),
        }

    def _get_ckd_stage(self, egfr: Optional[float]) -> str:
        if egfr is None:
            return "未知"
        if egfr >= 90:
            return "G1"
        if egfr >= 60:
            return "G2"
        if egfr >= 45:
            return "G3a"
        if egfr >= 30:
            return "G3b"
        if egfr >= 15:
            return "G4"
        return "G5"

    def _get_egfr_severity(self, egfr: Optional[float]) -> str:
        if egfr is None:
            return "未知"
        if egfr >= 90:
            return "肾功能基本正常或接近正常"
        if egfr >= 60:
            return "轻度下降"
        if egfr >= 45:
            return "轻中度下降"
        if egfr >= 30:
            return "中重度下降"
        if egfr >= 15:
            return "重度下降"
        return "肾功能衰竭高风险"

    def _determine_risk_level(
        self,
        abnormal_items: List[str],
        egfr: Optional[float],
        acr: Optional[float],
    ) -> str:
        if egfr is not None and egfr < 15:
            return "极高"
        if egfr is not None and egfr < 30:
            return "高"
        if acr is not None and acr >= 300:
            return "高"
        if len(abnormal_items) >= 4:
            return "高"
        if len(abnormal_items) >= 2:
            return "中"
        if len(abnormal_items) >= 1:
            return "低-中"
        return "低"

    def _build_summary(
        self,
        abnormal_items: List[str],
        ckd_stage: str,
        egfr_severity: str,
        risk_level: str,
    ) -> str:
        if not abnormal_items:
            return "规则分析未发现明显肾脏相关异常。"

        abnormal_text = "、".join(abnormal_items)
        return (
            f"规则分析提示存在肾脏相关异常，当前异常包括：{abnormal_text}。"
            f"结合 eGFR 表现，当前可参考 CKD 分期为 {ckd_stage}，"
            f"肾功能严重程度判断为：{egfr_severity}。"
            f"整体风险等级为：{risk_level}。"
        )