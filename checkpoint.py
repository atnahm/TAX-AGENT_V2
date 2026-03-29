import os
import psycopg2
from psycopg2.extras import RealDictCursor
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv

load_dotenv()

class CheckpointManager:
    """
    Manager for LangGraph state persistence using PostgreSQL.
    """
    def __init__(self):
        self.conn_str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tax_agent_db")
        
    def get_saver(self):
        """
        Returns a PostgresSaver for LangGraph.
        """
        # In a real environment, LangGraph's PostgresSaver uses this connection.
        # For now, we'll return the connection or the saver object.
        return PostgresSaver(self.conn_str)

    def initialize_ledger_table(self):
        """
        Ensures the SQL Ledger table (PostgreSQL) for audit trails exists.
        Every entry shares a UUID with Weaviate and Qdrant.
        """
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cur:
                # Mock immutable ledger table logic
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS audit_trail (
                        id UUID PRIMARY KEY,
                        timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                        node_name TEXT NOT NULL,
                        task_id TEXT NOT NULL,
                        state_snapshot JSONB,
                        approval_signature TEXT,
                        shared_id UUID NOT NULL
                    );
                """)
                conn.commit()

checkpoint_manager = CheckpointManager()
