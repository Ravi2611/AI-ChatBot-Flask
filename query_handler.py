import logging
import numpy as np
from embedding_index import EmbeddingIndex

logger = logging.getLogger("query_handler")

def query_embeddings(query, embedding_index: EmbeddingIndex, top_k=3):
    """
    Query the Postgres-backed embedding index and return top_k results.
    Each result includes the text, source file, and similarity score.
    """
    if not query or not isinstance(query, str):
        logger.warning("⚠️ Empty or invalid query provided.")
        return []

    try:
        results = embedding_index.query(query, top_k=top_k)
        if not results:
            logger.info(f"🔍 No matches found for query: '{query}'")
        else:
            logger.info(
                f"🔍 Query '{query}' → Top {len(results)} results (requested top_k={top_k})"
            )
        return results
    except Exception as e:
        logger.error(f"❌ Query failed for '{query}': {e}")
        return []
