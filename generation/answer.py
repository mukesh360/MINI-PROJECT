from generation.prompt import build_prompt
from generation.llm import LLM


class AnswerGenerator:
    def __init__(self, llm: LLM):
        self.llm = LLM()

    def generate(
        self,
        question: str,
        context: str,
        citations: list[dict],
    ) -> dict:
        prompt = build_prompt(question, context)

        answer = self.llm.generate(prompt)

        if "not found" in answer.lower():
            return {
                "answer": "Not found in the provided documents.",
                "citations": [],
            }

        return {
            "answer": answer,
            "citations": citations,
        }
