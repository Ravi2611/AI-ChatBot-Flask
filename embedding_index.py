import logging
import psycopg2
from embedding_model import embedding_model  # Preloaded SentenceTransformer
from db import get_connection  # Postgres connection helper

logger = logging.getLogger("embedding_index")
logger.setLevel(logging.INFO)


class EmbeddingIndex:
    """
    Handles embedding creation and storage in Postgres (pgvector).
    """

    def __init__(self):
        try:
            self.conn = get_connection()
            logger.info("✅ Database connection established")
        except Exception as e:
            self.conn = None
            logger.exception(f"❌ Failed to connect to DB: {e}")


    def add_texts(self, texts, file_name):
        """Add texts with embeddings to Postgres, inserting all rows, skipping exact duplicates."""
        added, skipped = 0, 0
        try:
            with self.conn.cursor() as cur:
                for t in texts:
                    # Encode embedding as numpy list
                    embedding = embedding_model.encode(t["text"], convert_to_numpy=True).tolist()
                    # Convert to Postgres vector string format
                    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

                    cur.execute(
                        """
                        INSERT INTO documents (file_name, content, embedding)
                        VALUES (%s, %s, %s::vector)
                        ON CONFLICT DO NOTHING
                        """,
                        (file_name, t["text"], embedding_str),
                    )

                    if cur.rowcount == 1:  # row inserted
                        added += 1
                    else:  # row skipped (duplicate)
                        skipped += 1

            self.conn.commit()
            logger.info(f"✅ {file_name}: Added {added}, Skipped {skipped}, Total {len(texts)}")
        except Exception as e:
            self.conn.rollback()
            logger.exception(f"❌ Error while storing embeddings for {file_name}: {e}")



    def check_file_exists(self, file_name: str) -> bool:
        """Check if a file already exists in the database."""
        try:
            with get_connection() as conn:  # fresh connection
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM documents WHERE file_name = %s LIMIT 1", (file_name,))
                    return cur.fetchone() is not None
        except Exception as e:
            logger.exception(f"❌ Error checking file existence for {file_name}: {e}")
            return False



    def query(self, query_text, top_k=5):
        """
        Query Postgres for top_k similar texts using pgvector.

        Returns:
            List[dict]: {'file_name', 'text', 'similarity'}
        """
        if not query_text.strip():
            logger.warning("⚠️ Empty query provided.")
            return []

        try:
            query_vec = embedding_model.encode(query_text, convert_to_numpy=True).tolist()
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT file_name, content, embedding <#> %s::vector AS distance
                    FROM documents
                    ORDER BY distance ASC
                    LIMIT %s
                    """,
                    (query_vec, top_k),
                )

                results = [
                    {
                        "file_name": file_name,
                        "text": content,
                        "similarity": float(1 - distance),  # convert distance to similarity
                    }
                    for file_name, content, distance in cur.fetchall()
                ]

            logger.info(f"🔍 Query complete. Top {len(results)} results returned.")
            return results

        except Exception as e:
            logger.exception(f"❌ Query failed for '{query_text}': {e}")
            return []

