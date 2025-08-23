# This script is to test the model backend functionality from the CLI


import logging
from embedding_index import EmbeddingIndex
from file_handler import process_existing_files
from query_handler import query_embeddings
from refine_answer import refine_answer
from config import WATCH_FOLDER

# -----------------------
# Setup logging
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("main")

embedding_index = EmbeddingIndex()

if __name__ == "__main__":
    # Step 1: Process all existing files in folder
    logger.info("Processing existing files in the watch folder...")
    logger.info(f"Watch folder: {WATCH_FOLDER}")
    process_existing_files(embedding_index)

    # Step 2: Query loop
    logger.info("Entering interactive query loop. Type 'exit' or 'quit' to stop.")
    while True:
        try:
            query = input("\nEnter your query: ")
            if query.lower() in ["exit", "quit"]:
                logger.info("Exiting program.")
                break

            logger.info(f"Received query: {query}")
            top_results = query_embeddings(query, embedding_index, top_k=3)

            if top_results:
                logger.debug(f"Top results: {top_results}")
                refined = refine_answer(query, top_results)
                print("\n✅ Refined Answer:")
                print(refined)
            else:
                logger.warning("No results found for the query.")

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt detected. Exiting.")
            break
        except Exception as e:
            logger.exception(f"Unexpected error while processing query: {e}")
