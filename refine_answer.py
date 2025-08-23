import logging
from transformers import pipeline

# -------------------------------
# Setup logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------------
# Load both models once
# -------------------------------
logger.info("Loading DistilBERT QA pipeline...")
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-uncased-distilled-squad"
)

logger.info("Loading Flan-T5 text2text pipeline...")
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device_map="auto"
)

# -------------------------------
# Hybrid Answer Function
# -------------------------------
def refine_answer(query, top_documents, confidence_threshold=0.3):
    """
    Hybrid answer refinement with logging:
    1. Try extractive QA (DistilBERT).
    2. If confidence too low or nonsense, fallback to Flan-T5.
    """
    context = "\n".join([doc['text'] for doc in top_documents])

    logger.info(f"Received query: {query}")
    logger.debug(f"Context length: {len(context)} characters")

    # Step 1: Try DistilBERT extractive QA
    result = qa_pipeline(question=query, context=context)
    answer = result.get("answer", "").strip()
    score = result.get("score", 0.0)

    logger.info(f"DistilBERT predicted: '{answer}' (score={score:.2f})")

    if score >= confidence_threshold and answer:
        logger.info("✅ Using DistilBERT answer (above confidence threshold)")
        return answer

    # Step 2: Fall back to Flan-T5 reasoning
    logger.warning("⚠️ DistilBERT confidence too low, falling back to Flan-T5...")
    prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        "If the answer is explicitly present in the context, provide a detailed response using all available information.\n"
        "If the answer is not present but you can make a reasonable guess based on the context, reply with your best estimate and explain your reasoning.\n"
        "If you cannot even guess, reply: 'I am not aware of this information.'"
    )
    gen_result = generator(prompt, max_new_tokens=300)
    final_answer = gen_result[0]['generated_text']

    logger.info("✅ Using Flan-T5 generated answer")
    return final_answer
