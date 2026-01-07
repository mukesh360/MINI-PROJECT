from generation.answer import AnswerGenerator


class DummyLLM:
    def generate(self, prompt: str) -> str:
        if "capital of france" in prompt.lower():
            return "Paris is the capital of France."
        return "Not found in the provided documents."


def test_answer_with_context():
    llm = DummyLLM()
    generator = AnswerGenerator(llm)

    result = generator.generate(
        question="What is the capital of France?",
        context="Paris is the capital of France.",
        citations=[{"chunk_id": "1"}],
    )

    assert result["answer"] == "Paris is the capital of France."
    assert len(result["citations"]) == 1


def test_answer_refusal():
    llm = DummyLLM()
    generator = AnswerGenerator(llm)

    result = generator.generate(
        question="Who is the president of Mars?",
        context="",
        citations=[],
    )

    assert result["answer"] == "Not found in the provided documents."
    assert result["citations"] == []
