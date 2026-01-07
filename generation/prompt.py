def build_prompt(
    question: str,
    context: str,
) -> str:
    """
    Strict RAG prompt.
    Model must refuse if answer is not in context.
    """

    return f"""You are a retrieval-augmented assistant.

Answer ONLY using the provided context.
If the answer is not found in the context, say:
"Not found in the provided documents."

Context:
{context}

Question:
{question}

Answer:"""
