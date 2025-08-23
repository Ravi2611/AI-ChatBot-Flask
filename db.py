import psycopg2
import logging
from config import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def init_db():
    """
    Initialize Postgres with pgvector and fix constraints.
    """
    try:
        conn = psycopg2.connect(Config.DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()

        # Enable pgvector extension
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

        # Create documents table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                file_name TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding vector(384)
            )
        """)

        # Drop old wrong unique constraint (file_name only)
        cur.execute("ALTER TABLE documents DROP CONSTRAINT IF EXISTS documents_file_name_key")

        # Add correct uniqueness (file_name + content)
        cur.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint WHERE conname = 'unique_file_content'
                ) THEN
                    ALTER TABLE documents
                    ADD CONSTRAINT unique_file_content UNIQUE (file_name, content);
                END IF;
            END$$;
        """)

        cur.close()
        conn.close()
        logger.info("✅ Database initialized successfully with fixed unique constraints.")

    except Exception as e:
        logger.exception(f"❌ Failed to initialize database: {e}")


def get_connection():
    return psycopg2.connect(Config.DATABASE_URL)
