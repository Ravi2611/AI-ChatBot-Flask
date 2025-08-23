import logging
from flask import Flask, request, jsonify
from embedding_index import EmbeddingIndex
from file_handler import process_existing_files
from query_handler import query_embeddings
from refine_answer import refine_answer
from config import WATCH_FOLDER
from db import init_db
from dotenv import load_dotenv
import os

# -----------------------
# Initialize database
# -----------------------
init_db()

# -----------------------
# Setup logging
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("app")

# -----------------------
# Initialize app + Postgres-backed index
# -----------------------
app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

# Build db_config from your existing .env
db_config = {
    'host': os.getenv('PGHOST'),
    'port': int(os.getenv('PGPORT')),
    'user': os.getenv('PGUSER'),
    'password': os.getenv('PGPASSWORD'),
    'dbname': os.getenv('PGDATABASE')
}
embedding_index = EmbeddingIndex()

# Process existing files at startup
logger.info("Processing existing files in the watch folder...")
logger.info(f"Watch folder: {WATCH_FOLDER}")
process_existing_files(embedding_index)

# -----------------------
# REST Endpoint
# -----------------------
@app.route("/query", methods=["POST"])
def query():
    """Handle a query request from Spring Boot or clients."""
    try:
        data = request.get_json()
        query_text = data.get("query")

        if not query_text:
            return jsonify({"error": "Query text is required"}), 400

        logger.info(f"Received query: {query_text}")
        top_results = query_embeddings(query_text, embedding_index, top_k=3)

        if not top_results:
            logger.warning("No results found for query.")
            return jsonify({"answer": "No relevant results found.", "sources": []}), 200

        refined = refine_answer(query_text, top_results)

        return jsonify({
            "answer": refined,
            "sources": top_results  # includes citations / doc refs
        }), 200

    except Exception as e:
        logger.exception(f"Error while processing query: {e}")
        return jsonify({"error": str(e)}), 500


# -----------------------
# Entry point
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
