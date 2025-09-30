import io
from typing import Any, Dict, List

import chardet
import pandas as pd
from fastapi import UploadFile
from .xml_reader import xml_to_dataframe


async def _read_file_detect_encoding(upload: UploadFile) -> bytes:
    content = await upload.read()
    return content


def _detect_encoding_and_sep(content: bytes) -> Dict[str, Any]:
    detection = chardet.detect(content)
    encoding = detection.get("encoding") or "utf-8"
    text_preview = content[:1000].decode(encoding, errors="ignore")
    sep = ","
    if "\t" in text_preview and text_preview.count("\t") > text_preview.count(","):
        sep = "\t"
    return {"encoding": encoding, "sep": sep}


def _profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    profile: Dict[str, Any] = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "columns_info": {},
        "potential_keys": [],
        "null_counts": {},
    }

    for col in df.columns:
        series = df[col]
        nulls = int(series.isna().sum())
        nunique = int(series.nunique(dropna=True))
        profile["columns_info"][str(col)] = {
            "dtype": str(series.dtype),
            "unique": nunique,
            "sample": series.dropna().head(3).tolist(),
        }
        profile["null_counts"][str(col)] = nulls
        if nunique == df.shape[0] and nulls == 0:
            profile["potential_keys"].append(str(col))

    return profile


def _looks_like_json(content: bytes) -> bool:
    s = content.lstrip()
    return s.startswith(b"{") or s.startswith(b"[")


async def profile_datasets(files: List[UploadFile]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for f in files:
        content = await _read_file_detect_encoding(f)
        meta = _detect_encoding_and_sep(content)
        encoding = meta["encoding"]
        name = f.filename or "file"

        # Prefer JSON for .json files or JSON-looking content; XML for .xml; otherwise CSV first
        prefer_json = (name.lower().endswith('.json')) or _looks_like_json(content)
        prefer_xml = name.lower().endswith('.xml')

        df = None
        if prefer_xml:
            try:
                df = xml_to_dataframe(content)
            except Exception:
                pass
            if df is None:
                try:
                    df = pd.read_csv(io.BytesIO(content), sep=meta["sep"])  # type: ignore[arg-type]
                except Exception:
                    pass
        elif prefer_json:
            # Try as JSON (array or object)
            try:
                df = pd.read_json(io.BytesIO(content))  # type: ignore[arg-type]
            except Exception:
                # Some JSONL cases
                try:
                    df = pd.read_json(io.BytesIO(content), lines=True)  # type: ignore[arg-type]
                except Exception:
                    pass
            # Fallback to CSV
            if df is None:
                try:
                    df = pd.read_csv(io.BytesIO(content), sep=meta["sep"])  # type: ignore[arg-type]
                except Exception:
                    pass
        else:
            # Try CSV first
            try:
                df = pd.read_csv(io.BytesIO(content), sep=meta["sep"])  # type: ignore[arg-type]
            except Exception:
                # Fallback to JSON/JSONL
                try:
                    df = pd.read_json(io.BytesIO(content))  # type: ignore[arg-type]
                except Exception:
                    try:
                        df = pd.read_json(io.BytesIO(content), lines=True)  # type: ignore[arg-type]
                    except Exception:
                        pass

        if df is None:
            results.append({
                "name": name,
                "detected": meta,
                "error": "Unsupported or unreadable file format",
            })
            continue

        profile = _profile_dataframe(df)
        results.append({
            "name": name,
            "detected": meta,
            "profile": profile,
        })

    return results


