from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[\wа-яА-Я]+", text.lower())


def _embed(text: str, dim: int = 256) -> List[float]:
    # Very light hashing embedding for MVP
    vec = [0.0] * dim
    for token in _tokenize(text):
        h = hash(token) % dim
        vec[h] += 1.0
    # L2 normalize
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def _cosine(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


_STORE: Dict[str, List[Tuple[str, List[float], Dict[str, Any]]]] = {}


def upsert(namespace: str, doc_id: str, text: str, metadata: Dict[str, Any]) -> None:
    emb = _embed(text)
    col = _STORE.setdefault(namespace, [])
    for i, (id_, _, _) in enumerate(col):
        if id_ == doc_id:
            col[i] = (doc_id, emb, metadata)
            return
    col.append((doc_id, emb, metadata))


def search(namespace: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    q = _embed(query)
    col = _STORE.get(namespace, [])
    scored = [
        {"id": id_, "score": _cosine(q, emb), "metadata": meta}
        for (id_, emb, meta) in col
    ]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[: top_k]


