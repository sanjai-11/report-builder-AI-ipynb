import tempfile
import unittest
from pathlib import Path

from report_builder.composer import compose_report
from report_builder.engine import ReportBuilder
from report_builder.models import AudienceMode, OutputKind, ReportConfig
from report_builder.parser import parse_outputs


class ReportBuilderTests(unittest.TestCase):
    def test_parse_outputs_mixed_types(self):
        payload = {
            "outputs": [
                {"type": "text", "title": "Key Observation", "value": "Sales increased 20%"},
                {"type": "table", "title": "KPI Table", "content": "Metric|Value\nRevenue|120"},
                {"type": "chart", "title": "Trend", "text": "Line chart: upward trend"},
            ]
        }
        outputs = parse_outputs(payload)
        self.assertEqual(len(outputs), 3)
        self.assertEqual(outputs[1].kind, OutputKind.TABLE)
        self.assertEqual(outputs[2].title, "Trend")

    def test_audience_summary_mode(self):
        outputs = parse_outputs({"outputs": [{"title": "Quality", "content": "good", "type": "text"}]})
        config = ReportConfig(title="Demo", audience=AudienceMode.BUSINESS)
        document = compose_report(outputs, config)
        self.assertIn("Business impact", document.executive_summary)

    def test_build_creates_pdf_and_docx(self):
        outputs = parse_outputs({"outputs": [{"title": "Result", "content": "Complete", "type": "text"}]})
        with tempfile.TemporaryDirectory() as td:
            config = ReportConfig(title="Integration Report", output_dir=Path(td), company_name="ACME")
            built = ReportBuilder().build(outputs=outputs, config=config)
            self.assertTrue(built["pdf"].exists())
            self.assertTrue(built["docx"].exists())


if __name__ == "__main__":
    unittest.main()
