from dataclasses import dataclass

from .models import AudienceMode, NotebookOutput


class AIAdapter:
    def summarize(self, output: NotebookOutput, audience: AudienceMode, max_sentences: int = 2) -> str:
        raise NotImplementedError


@dataclass(slots=True)
class RuleBasedAIAdapter(AIAdapter):
    def summarize(self, output: NotebookOutput, audience: AudienceMode, max_sentences: int = 2) -> str:
        if audience is AudienceMode.BUSINESS:
            summary = f"Business impact: {output.title} highlights measurable outcomes and decision signals."
        elif audience is AudienceMode.TECHNICAL:
            summary = f"Technical reading: {output.title} captures direct observed output with implementation-level context."
        else:
            summary = f"Joint review: {output.title} combines outcome focus with technical evidence from the notebook output."
        return " ".join(summary.split(".")[:max_sentences]).strip() + "."
