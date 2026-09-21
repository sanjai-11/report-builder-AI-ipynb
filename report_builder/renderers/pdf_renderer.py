from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from ..models import OutputKind, ReportDocument


def render_pdf(document: ReportDocument, destination: str | Path) -> Path:
    out_path = Path(destination)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    story = []

    if document.config.logo_path and Path(document.config.logo_path).exists():
        story.append(Image(str(document.config.logo_path), width=120, height=60))
        story.append(Spacer(1, 12))

    story.append(Paragraph(document.config.title, styles["Title"]))
    meta = f"{document.config.company_name} | Audience: {document.config.audience.value}"
    story.append(Paragraph(meta, styles["Normal"]))
    story.append(Spacer(1, 18))

    if document.executive_summary:
        story.append(Paragraph("Executive Summary", styles["Heading2"]))
        story.append(Paragraph(document.executive_summary, styles["BodyText"]))
        story.append(Spacer(1, 12))

    for output in document.outputs:
        story.append(Paragraph(output.title, styles["Heading3"]))
        if output.kind is OutputKind.TABLE:
            rows = [line.split("|") for line in output.content.splitlines() if line.strip()]
            if rows:
                table = Table(rows, hAlign="LEFT")
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF7")),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                            ("PADDING", (0, 0), (-1, -1), 4),
                        ]
                    )
                )
                story.append(table)
            else:
                story.append(Paragraph(output.content, styles["BodyText"]))
        else:
            story.append(Paragraph(output.content.replace("\n", "<br/>"), styles["BodyText"]))
        story.append(Spacer(1, 10))

    template = SimpleDocTemplate(str(out_path), pagesize=A4, title=document.config.title)
    template.build(story)
    return out_path
