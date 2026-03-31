from typing import Any, Dict, List, Optional


class TrendService:
    def analyze_trend(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        if len(records) < 2:
            return {
                "has_trend": False,
                "message": "历史记录不足，至少需要两次检测结果才能进行趋势分析。"
            }

        sorted_records = sorted(records, key=lambda x: x.get("timestamp", ""))

        scr_trend = self._compare_metric(sorted_records, "scr", higher_is_worse=True)
        egfr_trend = self._compare_metric(sorted_records, "egfr", higher_is_worse=False)
        acr_trend = self._compare_metric(sorted_records, "acr", higher_is_worse=True)
        sbp_trend = self._compare_metric(sorted_records, "sbp", higher_is_worse=True)
        dbp_trend = self._compare_metric(sorted_records, "dbp", higher_is_worse=True)

        summary = self._build_summary(scr_trend, egfr_trend, acr_trend, sbp_trend, dbp_trend)

        return {
            "has_trend": True,
            "scr_trend": scr_trend,
            "egfr_trend": egfr_trend,
            "acr_trend": acr_trend,
            "sbp_trend": sbp_trend,
            "dbp_trend": dbp_trend,
            "trend_summary": summary,
        }

    def _compare_metric(
        self,
        records: List[Dict[str, Any]],
        field: str,
        higher_is_worse: bool
    ) -> Dict[str, Any]:
        values = [r.get(field) for r in records if r.get(field) is not None]
        if len(values) < 2:
            return {
                "field": field,
                "status": "数据不足",
                "first_value": None,
                "last_value": None,
                "change": None,
            }

        first_value = values[0]
        last_value = values[-1]
        change = last_value - first_value

        if abs(change) < 1e-6:
            status = "基本稳定"
        else:
            if higher_is_worse:
                status = "恶化" if change > 0 else "改善"
            else:
                status = "改善" if change > 0 else "恶化"

        return {
            "field": field,
            "status": status,
            "first_value": first_value,
            "last_value": last_value,
            "change": round(change, 2),
        }

    def _build_summary(
        self,
        scr_trend: Dict[str, Any],
        egfr_trend: Dict[str, Any],
        acr_trend: Dict[str, Any],
        sbp_trend: Dict[str, Any],
        dbp_trend: Dict[str, Any],
    ) -> str:
        parts = []

        if scr_trend["status"] != "数据不足":
            parts.append(f"血肌酐趋势：{scr_trend['status']}")
        if egfr_trend["status"] != "数据不足":
            parts.append(f"eGFR趋势：{egfr_trend['status']}")
        if acr_trend["status"] != "数据不足":
            parts.append(f"尿白蛋白/肌酐比趋势：{acr_trend['status']}")
        if sbp_trend["status"] != "数据不足":
            parts.append(f"收缩压趋势：{sbp_trend['status']}")
        if dbp_trend["status"] != "数据不足":
            parts.append(f"舒张压趋势：{dbp_trend['status']}")

        if not parts:
            return "暂无足够历史数据进行趋势分析。"

        return "；".join(parts) + "。"