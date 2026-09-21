import argparse
from pathlib import Path

from .engine import ReportBuilder
from .models import AudienceMode, ReportConfig
from .parser import parse_outputs_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert notebook outputs into professional PDF and DOCX reports")
    parser.add_argument("--input", required=True, help="Path to notebook output JSON")
    parser.add_argument("--title", required=True, help="Report title")
    parser.add_argument("--author", default="", help="Report author")
    parser.add_argument("--company", default="", help="Company name")
    parser.add_argument("--audience", choices=[m.value for m in AudienceMode], default=AudienceMode.BUSINESS_TECHNICAL.value)
    parser.add_argument("--logo", default="", help="Optional path to company logo")
    parser.add_argument("--output-dir", default="reports", help="Directory for generated files")
    parser.add_argument("--no-ai-summary", action="store_true", help="Disable AI-generated executive summary")
    args = parser.parse_args()

    outputs = parse_outputs_file(args.input)
    config = ReportConfig(
        title=args.title,
        author=args.author,
        company_name=args.company,
        audience=AudienceMode(args.audience),
        logo_path=Path(args.logo) if args.logo else None,
        output_dir=Path(args.output_dir),
        include_ai_summary=not args.no_ai_summary,
    )
    builder = ReportBuilder()
    built = builder.build(outputs=outputs, config=config)
    print(f"Generated: {built['pdf']}")
    print(f"Generated: {built['docx']}")


if __name__ == "__main__":
    main()
