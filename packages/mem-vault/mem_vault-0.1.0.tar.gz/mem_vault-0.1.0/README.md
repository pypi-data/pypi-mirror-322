# Vector Memory

A Python library for efficient vector-based memory storage using PostgreSQL and pgvector. Perfect for LLM applications that need to maintain conversation context and retrieve relevant information.

## Features

- Vector similarity search using pgvector
- Easy PostgreSQL integration
- Conversation-based memory management
- Metadata support for rich memory context
- Bulk operations support
- Automatic cleanup of old conversations

## Installation

```bash
pip install vector-memory
```

### Prerequisites

1. PostgreSQL 11 or later
2. pgvector extension

To install pgvector on your PostgreSQL instance:
```sql
CREATE EXTENSION vector;
```

## Quick Start

```python
from vector_memory import VectorMemory, PostgresVectorStorage
from openai import OpenAI

# Initialize connection
memory = VectorMemory.initialize(
    host="localhost",
    port=5432,
    database="your_db",
    user="your_user",
    password="your_password",
    openai_api_key="your-openai-key"
)

# Add a memory
memory.add_memory(
    conversation_id="user_123",
    content="The user prefers dark mode in applications."
)

# Retrieve relevant memories
relevant_memories = memory.get_relevant_memories(
    conversation_id="user_123",
    query="What are the user's UI preferences?",
    limit=5
)

# Print retrieved memories
for memory in relevant_memories:
    print(memory['content'])
```

## Advanced Usage

### With Metadata

```python
# Add memory with metadata
memory.add_memory(
    conversation_id="user_123",
    content="User selected blue theme",
    metadata={
        "category": "preferences",
        "timestamp": "2024-01-18T10:30:00",
        "source": "settings_page"
    }
)

# Search with metadata filters
memories = memory.get_relevant_memories(
    conversation_id="user_123",
    query="What theme was selected?",
    filter_metadata={"category": "preferences"}
)
```

### Bulk Operations

```python
# Add multiple memories at once
contents = [
    "User opened dashboard",
    "User viewed reports",
    "User downloaded PDF"
]

metadata_list = [
    {"action": "view", "page": "dashboard"},
    {"action": "view", "page": "reports"},
    {"action": "download", "type": "pdf"}
]

memory.add_memories(
    conversation_id="user_123",
    contents=contents,
    metadata_list=metadata_list
)
```

### Memory Management

```python
# Delete a conversation
memory.delete_conversation("user_123")

# Clean up old conversations
memory.cleanup_old_conversations(days=30)

# Get conversation statistics
stats = memory.get_conversation_stats("user_123")
print(f"Total memories: {stats['total_memories']}")
print(f"Oldest memory: {stats['oldest_memory']}")
```

## Connection Management

### Basic Connection

```python
# Using connection parameters
memory = VectorMemory.initialize(
    host="localhost",
    port=5432,
    database="your_db",
    user="your_user",
    password="your_password",
    openai_api_key="your-openai-key"
)

# Using connection string
memory = VectorMemory.initialize_from_string(
    "postgresql://user:password@localhost/dbname",
    openai_api_key="your-openai-key"
)
```

### Connection Pool

```python
# Initialize with connection pool
memory = VectorMemory.initialize(
    host="localhost",
    port=5432,
    database="your_db",
    user="your_user",
    password="your_password",
    openai_api_key="your-openai-key",
    pool_size=5,
    max_overflow=10
)
```

## Configuration Options

```python
memory = VectorMemory.initialize(
    host="localhost",
    port=5432,
    database="your_db",
    user="your_user",
    password="your_password",
    openai_api_key="your-openai-key",
    
    # PostgreSQL options
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    
    # Memory options
    max_tokens=8191,         # Maximum tokens per content
    embedding_model="text-embedding-ada-002",  # OpenAI embedding model
)
```

## Error Handling

```python
from vector_memory.exceptions import StorageError

try:
    memory.add_memory(
        conversation_id="user_123",
        content="Some content"
    )
except StorageError as e:
    print(f"Failed to store memory: {e}")
```

## Best Practices

1. Use descriptive conversation IDs:
```python
conversation_id = f"user_{user_id}_session_{session_id}"
```

2. Include relevant metadata:
```python
metadata = {
    "source": "chat",
    "timestamp": datetime.now().isoformat(),
    "user_role": "admin",
    "context": "support_ticket_123"
}
```

3. Implement regular cleanup:
```python
# Run periodically (e.g., daily)
memory.cleanup_old_conversations(days=30)
```

4. Use appropriate similarity thresholds:
```python
memories = memory.get_relevant_memories(
    conversation_id="user_123",
    query="search query",
    threshold=0.7  # Adjust based on your needs (0-1)
)
```

## Performance Tips

1. Use bulk operations for multiple memories:
```python
memory.add_memories(conversation_id, contents, metadata_list)
```

2. Index important metadata fields:
```sql
CREATE INDEX idx_memory_category ON vector_entries USING btree ((metadata->>'category'));
```

3. Use connection pooling for high-traffic applications:
```python
memory = VectorMemory.initialize(
    # ... connection details ...
    pool_size=10,
    max_overflow=20
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.