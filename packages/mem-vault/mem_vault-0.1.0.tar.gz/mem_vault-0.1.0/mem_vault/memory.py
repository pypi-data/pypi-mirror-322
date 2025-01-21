"""
Vector Memory - A PostgreSQL-based vector memory system for LLM applications.
Provides efficient storage and retrieval of memories using pgvector for similarity search.
"""

from typing import List, Optional, Dict, Any
import logging
from datetime import datetime, timedelta
from openai import OpenAI

from .exceptions import StorageError
from .storage import PostgresVectorStorage

logger = logging.getLogger(__name__)

class VectorMemory:
    """
    A class to manage vector-based memory storage and retrieval.
    
    This class provides an interface for storing and retrieving memories using
    vector embeddings for similarity search. It works with PostgreSQL and pgvector
    for efficient vector operations.

    Attributes:
        storage: The storage backend (PostgreSQL with pgvector)
        embeddings: The embedding provider (e.g., OpenAI)
        max_tokens: Maximum tokens per content string
    """

    def __init__(self, 
                 storage: PostgresVectorStorage, 
                 embedding_provider: Any,
                 max_tokens: int = 8191) -> None:
        """
        Initialize the VectorMemory system.

        Args:
            storage: PostgreSQL storage backend instance
            embedding_provider: Provider for creating embeddings (e.g., OpenAI client)
            max_tokens: Maximum tokens per content string (default: 8191 for OpenAI)
        """
        self.storage = storage
        self.embeddings = embedding_provider
        self.max_tokens = max_tokens
        self.embedding_model = "text-embedding-ada-002"

    @classmethod
    def initialize(cls,
                  host: str,
                  port: int,
                  database: str,
                  user: str,
                  password: str,
                  openai_api_key: str,
                  pool_size: int = 5,
                  max_overflow: int = 10,
                  pool_timeout: int = 30,
                  max_tokens: int = 8191,
                  embedding_model: str = "text-embedding-ada-002") -> 'VectorMemory':
        """
        Initialize VectorMemory with connection parameters.

        Args:
            host: PostgreSQL host
            port: PostgreSQL port
            database: Database name
            user: Database user
            password: Database password
            openai_api_key: OpenAI API key
            pool_size: Connection pool size
            max_overflow: Maximum number of connections to create beyond pool_size
            pool_timeout: Seconds to wait for a connection from the pool
            max_tokens: Maximum tokens per content
            embedding_model: OpenAI embedding model name

        Returns:
            VectorMemory: Initialized instance
        """
        # Create connection string
        connection_string = (
            f"postgresql://{user}:{password}@{host}:{port}/{database}"
        )

        # Initialize storage with connection pool
        storage = PostgresVectorStorage(
            connection_string,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout
        )

        # Initialize OpenAI client
        openai_client = OpenAI(api_key=openai_api_key)

        # Create vector memory instance
        return cls(
            storage=storage,
            embedding_provider=openai_client,
            max_tokens=max_tokens
        )

    @classmethod
    def initialize_from_string(cls,
                             connection_string: str,
                             openai_api_key: str,
                             pool_size: int = 5,
                             max_overflow: int = 10,
                             pool_timeout: int = 30,
                             max_tokens: int = 8191,
                             embedding_model: str = "text-embedding-ada-002") -> 'VectorMemory':
        """
        Initialize VectorMemory with a connection string.

        Args:
            connection_string: PostgreSQL connection string
            openai_api_key: OpenAI API key
            pool_size: Connection pool size
            max_overflow: Maximum number of connections to create beyond pool_size
            pool_timeout: Seconds to wait for a connection from the pool
            max_tokens: Maximum tokens per content
            embedding_model: OpenAI embedding model name

        Returns:
            VectorMemory: Initialized instance
        """
        # Initialize storage with connection pool
        storage = PostgresVectorStorage(
            connection_string,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout
        )

        # Initialize OpenAI client
        openai_client = OpenAI(api_key=openai_api_key)

        # Create vector memory instance
        return cls(
            storage=storage,
            embedding_provider=openai_client,
            max_tokens=max_tokens
        )

    def _create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding using OpenAI's API.

        Args:
            text: Text to create embedding for

        Returns:
            List[float]: The embedding vector

        Raises:
            StorageError: If embedding creation fails
        """
        try:
            response = self.embeddings.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to create embedding: {str(e)}")
            raise StorageError(f"Failed to create embedding: {str(e)}")

    def add_memory(self, 
                  conversation_id: str, 
                  content: str, 
                  metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Add a single memory to storage.

        Args:
            conversation_id: Unique identifier for the conversation
            content: Text content to store
            metadata: Optional metadata dictionary to store with the memory

        Returns:
            bool: True if storage was successful

        Raises:
            StorageError: If storage operation fails
        """
        try:
            # Validate content length
            if not content or len(content) > self.max_tokens:
                raise ValueError(f"Content length must be between 1 and {self.max_tokens} tokens")

            # Create embedding
            embedding = self._create_embedding(content)
            if not embedding:
                raise StorageError("Failed to create embedding")

            # Store with metadata if provided
            return self.storage.store(
                conversation_id=conversation_id,
                content=content,
                embedding=embedding,
                metadata=metadata or {}
            )
        except ValueError:  # Let ValueError pass through
            raise
        except Exception as e:
            logger.error(f"Failed to add memory: {str(e)}")
            raise StorageError(f"Failed to add memory: {str(e)}")

    def _chunk_text(self, text: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks of approximately equal size.
        """
        if not text:
            return []
            
        if len(text) <= chunk_size:
            return [text]
            
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if end < len(text):
                # Try to find a paragraph break within the overlap range
                next_break = text.rfind('\n\n', end - overlap, end + overlap)
                if next_break != -1:
                    # Don't include the paragraph break at the end of the chunk
                    end = text.rfind('.', start, next_break) + 1 if text.rfind('.', start, next_break) != -1 else next_break
                else:
                    # Try to find a sentence break
                    next_period = text.rfind('.', end - overlap, end + overlap)
                    if next_period != -1:
                        end = next_period + 1
                    else:
                        # Last resort: break at a space
                        next_space = text.rfind(' ', end - overlap, end + overlap)
                        if next_space != -1:
                            # Try to find a period before the space
                            last_period = text.rfind('.', start, next_space)
                            if last_period != -1 and last_period > start:
                                end = last_period + 1
                            else:
                                end = next_space
            
            chunk = text[start:end].strip()
            if chunk:
                # Ensure chunk ends with a proper sentence if possible
                if not chunk.endswith('.') and '.' in chunk:
                    chunk = chunk[:chunk.rindex('.')+1]
                chunks.append(chunk)
            
            # Move start to the end of last complete sentence in previous chunk
            start = end
        
        return chunks

    def add_memories(self, 
                    conversation_id: str, 
                    contents: List[str],
                    metadata_list: Optional[List[Dict[str, Any]]] = None,
                    chunk_size: int = 2000,
                    chunk_overlap: int = 200) -> bool:
        """
        Add multiple memories at once, automatically chunking long content.
        
        Args:
            conversation_id: Unique identifier for the conversation
            contents: List of text contents to store
            metadata_list: Optional list of metadata dictionaries
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
            
        Returns:
            bool: True if all memories were stored successfully
            
        Raises:
            StorageError: If storage operation fails
        """
        try:
            entries = []
            metadata_list = metadata_list or [{}] * len(contents)
            
            # Validate input lengths
            if len(contents) != len(metadata_list):
                raise ValueError("Contents and metadata lists must be the same length")
                
            # Process each content item
            for content, metadata in zip(contents, metadata_list):
                if not content:
                    continue
                    
                # Determine if content needs chunking
                if len(content) > self.max_tokens:
                    chunks = self._chunk_text(content, chunk_size, chunk_overlap)
                    
                    # Update metadata for chunks
                    chunk_metadata = metadata.copy()
                    if 'chunks' not in chunk_metadata:
                        chunk_metadata['chunks'] = {
                            'total': len(chunks),
                            'original_length': len(content)
                        }
                    
                    # Process each chunk
                    for i, chunk in enumerate(chunks):
                        chunk_meta = chunk_metadata.copy()
                        chunk_meta['chunk'] = {
                            'index': i,
                            'total': len(chunks)
                        }
                        
                        embedding = self._create_embedding(chunk)
                        if not embedding:
                            raise StorageError(f"Failed to create embedding for chunk {i}")
                            
                        entries.append((conversation_id, chunk, embedding, chunk_meta))
                else:
                    # Process single content
                    embedding = self._create_embedding(content)
                    if not embedding:
                        raise StorageError(f"Failed to create embedding for content: {content[:100]}...")
                        
                    entries.append((conversation_id, content, embedding, metadata))
            
            return self.storage.bulk_store(entries)
            
        except Exception as e:
            logger.error(f"Failed to add memories in bulk: {str(e)}")
            raise StorageError(f"Failed to add memories in bulk: {str(e)}")

    def get_relevant_memories(self, 
                            conversation_id: str, 
                            query: str, 
                            limit: int = 5,
                            threshold: float = 0.7,
                            filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get memories relevant to a query.

        Args:
            conversation_id: Conversation to search within
            query: Query text to find similar memories
            limit: Maximum number of memories to return
            threshold: Minimum similarity threshold (0-1)
            filter_metadata: Optional metadata filters

        Returns:
            List[Dict[str, Any]]: List of relevant memories with their metadata

        Raises:
            StorageError: If search operation fails
        """
        try:
            # Create query embedding
            query_embedding = self._create_embedding(query)
            if not query_embedding:
                raise StorageError("Failed to create query embedding")

            # Search for similar memories
            results = self.storage.search_similar(
                conversation_id=conversation_id,
                query_embedding=query_embedding,
                limit=limit,
                threshold=threshold,
                filter_metadata=filter_metadata
            )

            return results
        except Exception as e:
            logger.error(f"Failed to get relevant memories: {str(e)}")
            raise StorageError(f"Failed to get relevant memories: {str(e)}")

    def get_all_memories(self, 
                        conversation_id: str,
                        filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get all memories for a conversation.

        Args:
            conversation_id: Conversation to retrieve
            filter_metadata: Optional metadata filters

        Returns:
            List[Dict[str, Any]]: List of all memories with their metadata

        Raises:
            StorageError: If retrieval operation fails
        """
        try:
            return self.storage.get_all(
                conversation_id=conversation_id,
                filter_metadata=filter_metadata
            )
        except Exception as e:
            logger.error(f"Failed to get all memories: {str(e)}")
            raise StorageError(f"Failed to get all memories: {str(e)}")

    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete an entire conversation.

        Args:
            conversation_id: Conversation to delete

        Returns:
            bool: True if deletion was successful

        Raises:
            StorageError: If deletion operation fails
        """
        try:
            return self.storage.delete_conversation(conversation_id)
        except Exception as e:
            logger.error(f"Failed to delete conversation: {str(e)}")
            raise StorageError(f"Failed to delete conversation: {str(e)}")

    def cleanup_old_conversations(self, days: int) -> bool:
        """
        Clean up conversations older than specified days.

        Args:
            days: Delete conversations older than this many days

        Returns:
            bool: True if cleanup was successful

        Raises:
            StorageError: If cleanup operation fails
        """
        try:
            if days < 1:
                raise ValueError("Days must be positive")
            return self.storage.cleanup_old_conversations(days)
        except Exception as e:
            logger.error(f"Failed to cleanup old conversations: {str(e)}")
            raise StorageError(f"Failed to cleanup old conversations: {str(e)}")

    def update_memory_metadata(self,
                             conversation_id: str,
                             content: str,
                             metadata: Dict[str, Any]) -> bool:
        """
        Update metadata for a specific memory.

        Args:
            conversation_id: Conversation ID
            content: Content of the memory to update
            metadata: New metadata to set

        Returns:
            bool: True if update was successful

        Raises:
            StorageError: If update operation fails
        """
        try:
            return self.storage.update_metadata(
                conversation_id=conversation_id,
                content=content,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"Failed to update memory metadata: {str(e)}")
            raise StorageError(f"Failed to update memory metadata: {str(e)}")

    def get_conversation_stats(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get statistics for a conversation.

        Args:
            conversation_id: Conversation to analyze

        Returns:
            Dict[str, Any]: Statistics about the conversation

        Raises:
            StorageError: If stats calculation fails
        """
        try:
            return self.storage.get_stats(conversation_id)
        except Exception as e:
            logger.error(f"Failed to get conversation stats: {str(e)}")
            raise StorageError(f"Failed to get conversation stats: {str(e)}")

    def get_memory_by_id(self, memory_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific memory by its ID.

        Args:
            memory_id: ID of the memory to retrieve

        Returns:
            Optional[Dict[str, Any]]: Memory data if found, None otherwise

        Raises:
            StorageError: If retrieval operation fails
        """
        try:
            return self.storage.get_by_id(memory_id)
        except Exception as e:
            logger.error(f"Failed to get memory by ID: {str(e)}")
            raise StorageError(f"Failed to get memory by ID: {str(e)}")