from .ai import AIAdapter, RuleBasedAIAdapter
from .models import NotebookOutput, ReportConfig, ReportDocument


def compose_report(outputs: list[NotebookOutput], config: ReportConfig, ai_adapter: AIAdapter | None = None) -> ReportDocument:
    adapter = ai_adapter or RuleBasedAIAdapter()
    executive_summary = ""
    if config.include_ai_summary and outputs:
        first_points = outputs[: min(3, len(outputs))]
        pieces = [adapter.summarize(output, config.audience, config.ai_summary_max_sentences) for output in first_points]
        executive_summary = " ".join(pieces)
    return ReportDocument(config=config, outputs=outputs, executive_summary=executive_summary)
