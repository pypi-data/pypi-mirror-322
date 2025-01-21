import pytest
from unittest.mock import Mock, patch
from mem_vault import VectorMemory
from mem_vault.exceptions import StorageError

# Mock data for testing
MOCK_EMBEDDING = [0.1] * 1536  # OpenAI embeddings are 1536-dimensional

@pytest.fixture
def mock_storage():
    storage = Mock()
    storage.store.return_value = True
    storage.bulk_store.return_value = True
    storage.search_similar.return_value = []
    storage.get_all.return_value = []
    storage.get_stats.return_value = {"total_memories": 0}
    return storage

@pytest.fixture
def mock_openai():
    openai = Mock()
    openai.embeddings.create.return_value = Mock(
        data=[Mock(embedding=MOCK_EMBEDDING)]
    )
    return openai

@pytest.fixture
def memory(mock_storage, mock_openai):
    return VectorMemory(
        storage=mock_storage,
        embedding_provider=mock_openai,
        max_tokens=8191
    )

class TestVectorMemory:
    def test_initialization(self, memory):
        """Test basic initialization"""
        assert memory.max_tokens == 8191
        assert memory.embedding_model == "text-embedding-ada-002"

    def test_create_embedding(self, memory):
        """Test embedding creation"""
        embedding = memory._create_embedding("test text")
        assert len(embedding) == 1536
        assert memory.embeddings.embeddings.create.called

    def test_add_single_memory(self, memory):
        """Test adding a single memory"""
        result = memory.add_memory(
            conversation_id="test_conv",
            content="test content",
            metadata={"test": "value"}
        )
        assert result == True
        memory.storage.store.assert_called_once()

    def test_add_memories_bulk(self, memory):
        """Test adding multiple memories"""
        contents = ["test1", "test2", "test3"]
        metadata_list = [{"id": i} for i in range(3)]
        
        result = memory.add_memories(
            conversation_id="test_conv",
            contents=contents,
            metadata_list=metadata_list
        )
        assert result == True
        memory.storage.bulk_store.assert_called_once()

    def test_chunking(self, memory):
        """Test text chunking functionality"""
        long_text = "a" * 3000  # Text longer than chunk_size
        chunks = memory._chunk_text(long_text, chunk_size=1000, overlap=100)
        
        assert len(chunks) > 1
        # Check overlap
        for i in range(len(chunks)-1):
            overlap = set(chunks[i][-100:]).intersection(set(chunks[i+1][:100]))
            assert len(overlap) > 0

    def test_add_long_content_with_chunking(self, memory):
        """Test adding content that requires chunking"""
        long_content = "a" * 10000  # Definitely needs chunking
        metadata = {"type": "test"}
        
        result = memory.add_memories(
            conversation_id="test_conv",
            contents=[long_content],
            metadata_list=[metadata],
            chunk_size=2000,
            chunk_overlap=200
        )
        
        assert result == True
        # Should have called bulk_store with multiple chunks
        args = memory.storage.bulk_store.call_args[0][0]
        assert len(args) > 1

    def test_get_relevant_memories(self, memory):
        """Test memory retrieval"""
        memory.storage.search_similar.return_value = [
            {"content": "test content", "metadata": {"score": 0.9}}
        ]
        
        results = memory.get_relevant_memories(
            conversation_id="test_conv",
            query="test query",
            limit=5,
            threshold=0.7
        )
        
        assert len(results) == 1
        assert results[0]["content"] == "test content"
        memory.storage.search_similar.assert_called_once()

    def test_get_all_memories(self, memory):
        """Test retrieving all memories"""
        memory.storage.get_all.return_value = [
            {"content": "test1"},
            {"content": "test2"}
        ]
        
        results = memory.get_all_memories("test_conv")
        assert len(results) == 2
        memory.storage.get_all.assert_called_once()

    def test_delete_conversation(self, memory):
        """Test conversation deletion"""
        memory.storage.delete_conversation.return_value = True
        result = memory.delete_conversation("test_conv")
        assert result == True
        memory.storage.delete_conversation.assert_called_once()

    def test_update_memory_metadata(self, memory):
        """Test metadata updates"""
        memory.storage.update_metadata.return_value = True
        result = memory.update_memory_metadata(
            conversation_id="test_conv",
            content="test content",
            metadata={"updated": True}
        )
        assert result == True
        memory.storage.update_metadata.assert_called_once()

    def test_get_conversation_stats(self, memory):
        """Test retrieving conversation statistics"""
        memory.storage.get_stats.return_value = {"total_memories": 5}
        stats = memory.get_conversation_stats("test_conv")
        assert stats["total_memories"] == 5
        memory.storage.get_stats.assert_called_once()

    def test_error_handling(self, memory):
        """Test error handling"""
        # Test invalid content length
        with pytest.raises(ValueError):
            memory.add_memory("test_conv", "")
        
        # Test embedding creation failure
        memory.embeddings.embeddings.create.side_effect = Exception("API Error")
        with pytest.raises(StorageError):
            memory.add_memory("test_conv", "test content")

    def test_metadata_preservation_in_chunks(self, memory):
        """Test that metadata is properly preserved and updated during chunking"""
        long_content = "a" * 10000
        original_metadata = {
            "type": "document",
            "author": "test",
            "priority": "high"
        }
        
        result = memory.add_memories(
            conversation_id="test_conv",
            contents=[long_content],
            metadata_list=[original_metadata],
            chunk_size=2000,
            chunk_overlap=200
        )
        
        # Check metadata in stored chunks
        stored_chunks = memory.storage.bulk_store.call_args[0][0]
        for chunk_data in stored_chunks:
            chunk_metadata = chunk_data[3]  # Metadata is the fourth element
            # Original metadata should be preserved
            assert chunk_metadata["type"] == original_metadata["type"]
            assert chunk_metadata["author"] == original_metadata["author"]
            # Chunk information should be added
            assert "chunk" in chunk_metadata
            assert "index" in chunk_metadata["chunk"]
            assert "total" in chunk_metadata["chunk"]

    @pytest.mark.parametrize("chunk_size,overlap", [
        (1000, 100),
        (2000, 200),
        (500, 50)
    ])
    def test_different_chunking_parameters(self, memory, chunk_size, overlap):
        """Test chunking with different parameters"""
        text = "a" * (chunk_size * 3)  # Create text that will need multiple chunks
        
        chunks = memory._chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        
        # Verify chunk sizes
        for chunk in chunks:
            assert len(chunk) <= chunk_size + overlap
            
        # Verify number of chunks
        expected_chunks = (len(text) - overlap) // (chunk_size - overlap)
        assert abs(len(chunks) - expected_chunks) <= 1

    def test_natural_language_chunking(self, memory):
        """Test chunking with natural language breaks"""
        text = """First paragraph with some content.

        Second paragraph with different content.
        
        Third paragraph with more content."""
        
        chunks = memory._chunk_text(text, chunk_size=50, overlap=10)
        
        # Check if chunks break at natural points
        for chunk in chunks[:-1]:  # Exclude last chunk
            assert chunk.endswith((".", "\n")) or chunk.strip().endswith(".")

if __name__ == "__main__":
    pytest.main([__file__])