# core/tutor.py

from typing import Optional
from core.llm import MistralLLM


class Tutor:
    """
    High-level teaching logic for OffTute.
    Converts user queries into student-friendly explanations.
    """

    def __init__(
        self,
        llm: Optional[MistralLLM] = None,
        language: str = "English",
        level: str = "beginner",
    ):
        self.llm = llm or MistralLLM()
        self.language = language
        self.level = level

    def _system_prompt(self) -> str:
        """
        Defines how OffTute should behave as a tutor.
        """

        return f"""
You are OffTute, a calm and friendly personal tutor.

Teaching rules:
- Explain concepts in VERY SIMPLE language
- Assume the student is a {self.level}
- Use step-by-step explanations
- Give real-life examples when possible
- Avoid unnecessary technical jargon
- Keep answers short and clear
- Respond only in {self.language}

If the topic is technical, break it into small parts.
If the student seems confused, re-explain more simply.
"""

    def explain(self, question: str) -> str:
        """
        Explain a concept in a student-friendly way.
        """

        return self.llm.generate(
            prompt=question,
            system_prompt=self._system_prompt(),
        )
