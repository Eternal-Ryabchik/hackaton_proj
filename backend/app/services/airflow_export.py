from __future__ import annotations

from typing import Any, Dict, List


def dag_from_steps(dag_id: str, steps: List[Dict[str, Any]]) -> str:
    lines = [
        "from airflow import DAG",
        "from airflow.operators.python import PythonOperator",
        "from datetime import datetime",
        "\n",
        f"with DAG(dag_id='{dag_id}', start_date=datetime(2024,1,1), schedule='@daily', catchup=False) as dag:",
    ]
    for i, step in enumerate(steps):
        task_id = f"step_{i}_{step.get('op')}"
        py = (
            "def _task(**context):\n"
            f"    print('Executing {step.get('op')} with params', {step})\n"
        )
        lines.append(py)
        lines.append(
            f"    t{i} = PythonOperator(task_id='{task_id}', python_callable=_task)"
        )
        if i > 0:
            lines.append(f"    t{i-1} >> t{i}")
    return "\n".join(lines) + "\n"


