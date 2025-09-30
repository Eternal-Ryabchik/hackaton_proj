import io
from typing import Any, Dict

import pandas as pd


def xml_to_dataframe(content: bytes) -> pd.DataFrame:
    try:
        # pandas will infer the table; users can refine later
        return pd.read_xml(io.BytesIO(content))  # type: ignore[arg-type]
    except Exception as e:
        # Fallback: try read_xml with parser/stylesheet disabled
        return pd.read_xml(io.BytesIO(content), xpath=".//*")  # type: ignore[arg-type]


