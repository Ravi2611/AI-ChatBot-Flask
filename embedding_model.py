import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("embedding_model")
logger.setLevel(logging.INFO)

logger.info("🔧 Loading embedding model (all-MiniLM-L6-v2)...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
logger.info("✅ Embedding model loaded successfully.")
