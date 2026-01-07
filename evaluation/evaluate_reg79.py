import time
from typing import List

# -----------------------------
# EVALUATION QUESTIONS
# (derived from UN Regulation 79)
# -----------------------------
EVAL_SET = [
    {
        "question": "What is the scope of UN Regulation No. 79?",
        "keywords": ["steering equipment", "vehicles", "categories m n o"]
    },
    {
        "question": "Define Advanced Driver Assistance Steering System.",
        "keywords": ["driver remains", "primary control", "assistance"]
    },
    {
        "question": "What is an Autonomous Steering System?",
        "keywords": ["off-board", "external signals", "no driver"]
    },
    {
        "question": "Which vehicle categories are covered under Regulation 79?",
        "keywords": ["category m", "category n", "category o"]
    },
    {
        "question": "What happens if a failure occurs in the steering system?",
        "keywords": ["warning", "failure", "steering control"]
    }
]

TOP_K = 3

# -----------------------------
# UTILS
# -----------------------------
def contains_keywords(text: str, keywords: List[str]) -> bool:
    text = text.lower()
    return any(k.lower() in text for k in keywords)

# -----------------------------
# RETRIEVAL METRIC
# -----------------------------
def evaluate_retrieval(retriever):
    hits = 0

    for item in EVAL_SET:
        chunks = retriever.retrieve(item["question"], top_k=TOP_K)

        if any(contains_keywords(chunk, item["keywords"]) for chunk in chunks):
            hits += 1

    return hits / len(EVAL_SET)

# -----------------------------
# ANSWER QUALITY (AUTOMATED)
# -----------------------------
def evaluate_answer_quality(llm, retriever):
    scores = []

    for item in EVAL_SET:
        chunks = retriever.retrieve(item["question"], top_k=TOP_K)
        context = "\n".join(chunks)

        prompt = f"""
        Answer the question strictly using the regulation text.

        Context:
        {context}

        Question:
        {item['question']}
        """

        answer = llm.generate(prompt)

        keyword_score = sum(
            1 for k in item["keywords"] if k.lower() in answer.lower()
        )

        normalized_score = keyword_score / len(item["keywords"])
        scores.append(normalized_score)

        print("\nQ:", item["question"])
        print("A:", answer[:400], "...")
        print("Keyword Score:", round(normalized_score, 2))

    return sum(scores) / len(scores)

# -----------------------------
# PERFORMANCE METRIC
# -----------------------------
def evaluate_latency(llm, retriever):
    times = []

    for item in EVAL_SET:
        start = time.time()
        chunks = retriever.retrieve(item["question"], top_k=TOP_K)
        context = "\n".join(chunks)
        llm.generate(context)
        times.append(time.time() - start)

    return sum(times) / len(times)

# -----------------------------
# MAIN
# -----------------------------
def run_evaluation(llm, retriever):
    print("\n--- Evaluating UN Regulation No. 79 RAG System ---")

    retrieval_acc = evaluate_retrieval(retriever)
    answer_score = evaluate_answer_quality(llm, retriever)
    latency = evaluate_latency(llm, retriever)

    print("\n========== FINAL METRICS ==========")
    print(f"Retrieval Accuracy      : {retrieval_acc * 100:.2f}%")
    print(f"Answer Faithfulness     : {answer_score * 100:.2f}%")
    print(f"Average Response Time   : {latency:.2f} seconds")
    print("===================================")
