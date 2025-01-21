"""
PostgreSQL storage implementation with pgvector support
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector

Base = declarative_base()


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    v1_array = np.array(v1)
    v2_array = np.array(v2)
    dot_product = np.dot(v1_array, v2_array)
    norm1 = np.linalg.norm(v1_array)
    norm2 = np.linalg.norm(v2_array)
    return dot_product / (norm1 * norm2)


class VectorEntry(Base):
    """Database model for vector entries"""
    __tablename__ = 'vector_entries'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    embedding = Column(Vector(1536))  # OpenAI's embedding size
    conversation_id = Column(String)
    memory_metadata = Column(JSON, default={})  # Changed from metadata to memory_metadata
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_conversation_id', 'conversation_id'),
        Index('idx_embedding_cosine_ops', embedding, postgresql_using='ivfflat'),
    )

class PostgresVectorStorage:
    """PostgreSQL storage backend with pgvector support"""

    def __init__(self, 
                 connection_string: str,
                 pool_size: int = 5,
                 max_overflow: int = 10,
                 pool_timeout: int = 30):
        """Initialize PostgreSQL storage"""
        self.engine = create_engine(
            connection_string,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout
        )

        # Create pgvector extension if it doesn't exist
        with self.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def store(self, 
              conversation_id: str, 
              content: str, 
              embedding: List[float],
              metadata: Dict[str, Any] = None) -> bool:
        """Store a single memory entry"""
        try:
            session = self.Session()
            entry = VectorEntry(
                conversation_id=conversation_id,
                content=content,
                embedding=embedding,
                memory_metadata=metadata or {}  # Changed to memory_metadata
            )
            session.add(entry)
            session.commit()
            session.close()
            return True
        except Exception as e:
            session.rollback()
            raise e

    def bulk_store(self, entries: List[tuple]) -> bool:
        """Store multiple memory entries"""
        try:
            session = self.Session()
            for conversation_id, content, embedding, metadata in entries:
                entry = VectorEntry(
                    conversation_id=conversation_id,
                    content=content,
                    embedding=embedding,
                    memory_metadata=metadata or {}  # Changed to memory_metadata
                )
                session.add(entry)
            session.commit()
            session.close()
            return True
        except Exception as e:
            session.rollback()
            raise e

    def search_similar(self,
                      conversation_id: str,
                      query_embedding: List[float],
                      limit: int = 5,
                      threshold: float = 0.7,
                      filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar memories"""
        try:
            session = self.Session()
            query = session.query(VectorEntry).filter(
                VectorEntry.conversation_id == conversation_id
            )

            if filter_metadata:
                for key, value in filter_metadata.items():
                    query = query.filter(VectorEntry.memory_metadata[key].astext == str(value))

            # Get all entries and calculate similarity
            entries = query.all()
            results = []
            
            for entry in entries:
                similarity = cosine_similarity(entry.embedding, query_embedding)
                if similarity >= threshold:
                    results.append({
                        "id": entry.id,
                        "content": entry.content,
                        "metadata": entry.memory_metadata,
                        "similarity": float(similarity),
                        "timestamp": entry.timestamp.isoformat()
                    })
            
            # Sort by similarity and limit results
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:limit]

        except Exception as e:
            session.rollback()
            raise e

    def get_all(self,
                conversation_id: str,
                filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all memories for a conversation"""
        try:
            session = self.Session()
            query = session.query(VectorEntry).filter(
                VectorEntry.conversation_id == conversation_id
            )

            if filter_metadata:
                for key, value in filter_metadata.items():
                    query = query.filter(VectorEntry.memory_metadata[key].astext == str(value))  # Changed to memory_metadata

            entries = query.all()
            results = [{
                "id": entry.id,
                "content": entry.content,
                "metadata": entry.memory_metadata,  # Changed but keeping the response format
                "timestamp": entry.timestamp.isoformat()
            } for entry in entries]

            session.close()
            return results
        except Exception as e:
            session.rollback()
            raise e

    def update_metadata(self,
                       conversation_id: str,
                       content: str,
                       metadata: Dict[str, Any]) -> bool:
        """Update metadata for a specific memory"""
        try:
            session = self.Session()
            entry = session.query(VectorEntry).filter(
                VectorEntry.conversation_id == conversation_id,
                VectorEntry.content == content
            ).first()

            if entry:
                entry.memory_metadata = metadata  # Changed to memory_metadata
                session.commit()
                session.close()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e

    # Other methods remain the same but use memory_metadata instead of metadata
    def get_stats(self, conversation_id: str) -> Dict[str, Any]:
        """Get statistics for a conversation.

        Args:
            conversation_id: Conversation to analyze

        Returns:
            Dict[str, Any]: Statistics about the conversation
        """
        try:
            session = self.Session()
            total_memories = session.query(VectorEntry).filter(
                VectorEntry.conversation_id == conversation_id
            ).count()

            oldest = session.query(VectorEntry).filter(
                VectorEntry.conversation_id == conversation_id
            ).order_by(VectorEntry.timestamp.asc()).first()

            newest = session.query(VectorEntry).filter(
                VectorEntry.conversation_id == conversation_id
            ).order_by(VectorEntry.timestamp.desc()).first()

            stats = {
                "total_memories": total_memories,
                "oldest_memory": oldest.timestamp.isoformat() if oldest else None,
                "newest_memory": newest.timestamp.isoformat() if newest else None,
                "conversation_id": conversation_id
            }

            session.close()
            return stats
        except Exception as e:
            session.rollback()
            raise e

    def get_by_id(self, memory_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific memory by ID"""
        try:
            session = self.Session()
            entry = session.query(VectorEntry).get(memory_id)
            
            if not entry:
                return None

            result = {
                "id": entry.id,
                "content": entry.content,
                "metadata": entry.memory_metadata,  # Changed but keeping the response format
                "conversation_id": entry.conversation_id,
                "timestamp": entry.timestamp.isoformat()
            }

            session.close()
            return result
        except Exception as e:
            session.rollback()
            raise e

    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete all memories for a conversation"""
        try:
            session = self.Session()
            session.query(VectorEntry).filter(
                VectorEntry.conversation_id == conversation_id
            ).delete()
            session.commit()
            session.close()
            return True
        except Exception as e:
            session.rollback()
            raise e

    def cleanup_old_conversations(self, days: int) -> bool:
        """Delete conversations older than specified days"""
        try:
            session = self.Session()
            session.query(VectorEntry).filter(
                VectorEntry.timestamp < text(f"NOW() - INTERVAL '{days} days'")
            ).delete()
            session.commit()
            session.close()
            return True
        except Exception as e:
            session.rollback()
            raise e
        