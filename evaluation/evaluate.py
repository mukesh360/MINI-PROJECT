import time
from typing import List

from generation.llm import LLM
from retrieval.pipeline import RetrievalPipeline


# ---------------------------
# EVALUATION QUESTIONS
# (based on your document)
# ---------------------------
EVAL_SET = [
    {
        "question": "What is the scope of UN Regulation No. 79?",
        "keywords": ["steering equipment", "vehicles", "categories m n o"]
    },
    {
        "question": "Which vehicle categories does UN Regulation No. 79 apply to?",
        "keywords": ["category m", "category n", "category o"]
    },
    {
        "question": "What types of steering systems are excluded from the scope of this regulation?",
        "keywords": ["purely pneumatic", "autonomous steering", "excluded"]
    },
    {
        "question": "What is meant by steering equipment according to the regulation?",
        "keywords": ["steering control", "steering transmission", "steered wheels", "energy supply"]
    },
    {
        "question": "What is an Advanced Driver Assistance Steering System?",
        "keywords": ["driver", "assistance", "primary control"]
    },
    {
        "question": "What is an Autonomous Steering System?",
        "keywords": ["off-board", "external signals", "not permitted"]
    },
    {
        "question": "What are Automatically Commanded Steering Functions (ACSF)?",
        "keywords": ["automatic", "electronic control", "assist the driver"]
    },
    {
        "question": "What is a Corrective Steering Function?",
        "keywords": ["correct", "lane departure", "vehicle stability"]
    },
    {
        "question": "What happens when a failure occurs in a non-mechanical steering transmission?",
        "keywords": ["warning", "driver", "failure"]
    },
    {
        "question": "What warning signals are required for steering system failures?",
        "keywords": ["optical warning", "acoustic warning", "driver"]
    },
    {
        "question": "What requirements apply when the steering system shares an energy source with the braking system?",
        "keywords": ["priority", "steering", "braking performance"]
    },
    {
        "question": "What is required for approval of a vehicle type under this regulation?",
        "keywords": ["type approval", "technical service", "tests"]
    }
]


TOP_K = 5


# ---------------------------
# UTILS
# ---------------------------
def keyword_match(text: str, keywords: List[str]) -> bool:
    text = text.lower()
    return any(k.lower() in text for k in keywords)


# ---------------------------
# RETRIEVAL EVALUATION
# ---------------------------
def evaluate_retrieval(pipeline: RetrievalPipeline):
    hits = 0

    for item in EVAL_SET:
        results = pipeline.search(item["question"])[:TOP_K]

        found = False
        for r in results:
            if keyword_match(r.get("text", ""), item["keywords"]):
                found = True
                break

        if found:
            hits += 1

    return hits / len(EVAL_SET)


# ---------------------------
# ANSWER QUALITY (AUTOMATED)
# ---------------------------
def evaluate_answer_quality(llm: LLM, pipeline: RetrievalPipeline):
    scores = []

    for item in EVAL_SET:
        results = pipeline.search(item["question"])[:TOP_K]
        context = "\n".join(r["text"] for r in results)

        prompt = f"""
        Answer the question strictly using the context below.
        Do not add external information.

        Context:
        {context}

        Question:
        {item['question']}
        """

        answer = llm.generate(prompt)

        keyword_hits = sum(
            1 for k in item["keywords"]
            if k.lower() in answer.lower()
        )

        score = keyword_hits / len(item["keywords"])
        scores.append(score)

        print("\nQ:", item["question"])
        print("A:", answer[:300], "...")
        print("Keyword score:", round(score, 2))

    return sum(scores) / len(scores)


# ---------------------------
# LATENCY
# ---------------------------
def evaluate_latency(llm: LLM, pipeline: RetrievalPipeline):
    times = []

    for item in EVAL_SET:
        start = time.time()
        results = pipeline.search(item["question"])[:TOP_K]
        context = "\n".join(r["text"] for r in results)
        llm.generate(context)
        times.append(time.time() - start)

    return sum(times) / len(times)


# ---------------------------
# MAIN
# ---------------------------
def main():
    pipeline = RetrievalPipeline(top_k=TOP_K)
    llm = LLM()

    print("\n--- Evaluating Retrieval Pipeline ---")
    retrieval_acc = evaluate_retrieval(pipeline)

    print("\n--- Evaluating Answer Quality ---")
    answer_score = evaluate_answer_quality(llm, pipeline)

    print("\n--- Evaluating System Performance ---")
    avg_latency = evaluate_latency(llm, pipeline)

    print("\n========== FINAL RESULTS ==========")
    print(f"Retrieval Accuracy     : {retrieval_acc * 100:.2f}%")
    print(f"Answer Faithfulness    : {answer_score * 100:.2f}%")
    print(f"Avg Response Time      : {avg_latency:.2f} sec")
    print("===================================")


if __name__ == "__main__":
    main()
