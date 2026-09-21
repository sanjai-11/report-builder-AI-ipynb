from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class OutputKind(str, Enum):
    TEXT = "text"
    TABLE = "table"
    CHART = "chart"
    IMAGE = "image"


class AudienceMode(str, Enum):
    BUSINESS = "business"
    TECHNICAL = "technical"
    BUSINESS_TECHNICAL = "business_technical"


@dataclass(slots=True)
class NotebookOutput:
    kind: OutputKind
    title: str
    content: str


@dataclass(slots=True)
class ReportConfig:
    title: str
    author: str = ""
    company_name: str = ""
    logo_path: Path | None = None
    audience: AudienceMode = AudienceMode.BUSINESS_TECHNICAL
    output_dir: Path = Path("reports")
    include_ai_summary: bool = True
    ai_summary_max_sentences: int = 2


@dataclass(slots=True)
class ReportDocument:
    config: ReportConfig
    outputs: list[NotebookOutput] = field(default_factory=list)
    executive_summary: str = ""
