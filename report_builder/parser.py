import json
from pathlib import Path

from .models import NotebookOutput, OutputKind


def _kind_from_string(value: str) -> OutputKind:
    normalized = value.strip().lower()
    if normalized in {"text", "markdown"}:
        return OutputKind.TEXT
    if normalized in {"table", "dataframe"}:
        return OutputKind.TABLE
    if normalized in {"chart", "plot"}:
        return OutputKind.CHART
    if normalized in {"image", "visualization", "viz"}:
        return OutputKind.IMAGE
    return OutputKind.TEXT


def parse_outputs(payload: dict) -> list[NotebookOutput]:
    raw_outputs = payload.get("outputs") or payload.get("results") or payload.get("cells") or []
    parsed: list[NotebookOutput] = []
    for idx, item in enumerate(raw_outputs, start=1):
        if not isinstance(item, dict):
            continue
        kind = _kind_from_string(str(item.get("kind") or item.get("type") or "text"))
        title = str(item.get("title") or f"Output {idx}")
        content = str(item.get("content") or item.get("value") or item.get("text") or "")
        parsed.append(NotebookOutput(kind=kind, title=title, content=content))
    return parsed


def parse_outputs_file(path: str | Path) -> list[NotebookOutput]:
    with Path(path).open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return parse_outputs(payload)
