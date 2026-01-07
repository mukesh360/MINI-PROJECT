from retrieval.pipeline import RetrievalPipeline
from retrieval.context_builder import ContextBuilder
from generation.answer import AnswerGenerator
from generation.llm import LLM


def run_query(question: str):
    # 1️⃣ Retrieve relevant chunks
    retriever = RetrievalPipeline()
    retrieved = retriever.search(question)

    # retrieved example:
    # [
    #   {"chunk_id": "...", "text": "...", "score": 0.72, "metadata": {...}},
    #   {"chunk_id": "...", "text": "...", "score": 0.61, "metadata": {...}},
    # ]

    # 2️⃣ Confidence gate
    if len(retrieved) < 2 or retrieved[0]["score"] < 0.35:
        return {
            "answer": "Not found in documents",
            "citations": [],
        }

    # 3️⃣ Build context (token-budget aware)
    context_builder = ContextBuilder(max_tokens=1500)
    context, citations = context_builder.build(retrieved)

    # 4️⃣ Generate answer
    llm = LLM()  # or local model
    generator = AnswerGenerator(llm)

    result = generator.generate(
        question=question,
        context=context,
        citations=citations,
    )

    return result


if __name__ == "__main__":
    response = run_query(
        "Full-power steering equipment"
    )

    print("\nAnswer:\n", response["answer"])
    print("\nCitations:")
    for c in response["citations"]:
        print(c)
