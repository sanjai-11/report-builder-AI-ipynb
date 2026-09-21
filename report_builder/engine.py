from pathlib import Path

from .ai import AIAdapter
from .composer import compose_report
from .models import NotebookOutput, ReportConfig
from .renderers.docx_renderer import render_docx
from .renderers.pdf_renderer import render_pdf


class ReportBuilder:
    def __init__(self, ai_adapter: AIAdapter | None = None):
        self.ai_adapter = ai_adapter

    def build(self, outputs: list[NotebookOutput], config: ReportConfig) -> dict[str, Path]:
        document = compose_report(outputs=outputs, config=config, ai_adapter=self.ai_adapter)
        config.output_dir.mkdir(parents=True, exist_ok=True)

        slug = config.title.lower().replace(" ", "-")
        pdf_path = render_pdf(document, config.output_dir / f"{slug}.pdf")
        docx_path = render_docx(document, config.output_dir / f"{slug}.docx")
        return {"pdf": pdf_path, "docx": docx_path}
