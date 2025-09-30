from __future__ import annotations

from typing import Any, Dict, List, Tuple


def suggest_join_keys(profile_left: Dict[str, Any], profile_right: Dict[str, Any]) -> List[Tuple[str, str, float]]:
    # Simple heuristic: match identical names; fallback to names containing 'id'
    cols_left = list(profile_left.get('columns_info', {}).keys())
    cols_right = list(profile_right.get('columns_info', {}).keys())
    suggestions: List[Tuple[str, str, float]] = []
    for l in cols_left:
        if l in cols_right:
            suggestions.append((l, l, 0.95))
    if not suggestions:
        lids = [c for c in cols_left if 'id' in c.lower()]
        rids = [c for c in cols_right if 'id' in c.lower()]
        for l in lids:
            for r in rids:
                suggestions.append((l, r, 0.8))
    return suggestions


def build_data_contract(profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": profile.get("name", "dataset"),
        "columns": [
            {
                "name": col,
                "type": info.get("dtype", "string"),
                "nullable": (profile.get("null_counts", {}).get(col, 0) > 0)
            } for col, info in profile.get("columns_info", {}).items()
        ],
        "constraints": {
            "primary_keys": profile.get("potential_keys", [])
        }
    }


