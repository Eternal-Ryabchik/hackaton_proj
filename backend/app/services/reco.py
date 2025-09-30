from __future__ import annotations

from typing import Any, Dict, List


def recommend_storage(profile: Dict[str, Any]) -> Dict[str, Any]:
    rows = profile.get("rows", 0)
    columns = profile.get("columns", 0)
    # Very simple heuristics for MVP
    if rows > 5_000_000:
        return {
            "system": "HDFS",
            "reason": "Большой объем (мультимиллионы строк) лучше хранить в распределенной файловой системе",
            "details": {"partition_by": "dt", "format": "parquet"},
        }
    if rows > 200_000:
        return {
            "system": "ClickHouse",
            "reason": "Аналитические агрегации по большим наборам быстрее в столбцовом хранилище",
            "details": {"partition_by": "dt", "order_by": "(user_id)"},
        }
    return {
        "system": "PostgreSQL",
        "reason": "Умеренный объем и оперативный доступ",
        "details": {"indexes": ["user_id"]},
    }


def generate_postgres_ddl(table: str, columns_info: Dict[str, Any]) -> str:
    col_lines: List[str] = []
    for name, info in columns_info.items():
        dtype = str(info.get("dtype", "text")).lower()
        if "int" in dtype:
            sql_type = "bigint"
        elif "float" in dtype or "double" in dtype:
            sql_type = "double precision"
        elif "datetime" in dtype or "date" in dtype:
            sql_type = "timestamp"
        else:
            sql_type = "text"
        col_lines.append(f"\t\"{name}\" {sql_type}")
    ddl = f"CREATE TABLE IF NOT EXISTS {table} (\n" + ",\n".join(col_lines) + "\n);"
    return ddl


def generate_clickhouse_ddl(table: str, columns_info: Dict[str, Any]) -> str:
    col_lines: List[str] = []
    for name, info in columns_info.items():
        dtype = str(info.get("dtype", "String")).lower()
        if "int" in dtype:
            sql_type = "Int64"
        elif "float" in dtype or "double" in dtype:
            sql_type = "Float64"
        elif "datetime" in dtype or "date" in dtype:
            sql_type = "DateTime"
        else:
            sql_type = "String"
        col_lines.append(f"\t`{name}` {sql_type}")
    ddl = (
        f"CREATE TABLE IF NOT EXISTS {table} (\n" + ",\n".join(col_lines) +
        "\n) ENGINE = MergeTree ORDER BY tuple()" 
    )
    return ddl


