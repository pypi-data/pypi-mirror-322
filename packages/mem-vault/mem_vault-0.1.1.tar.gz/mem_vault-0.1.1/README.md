# Mem Vault

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
pip install mem-vault
```

### Prerequisites

1. PostgreSQL 11 or later
2. pgvector extension

Install pgvector on your PostgreSQL instance:
```sql
CREATE EXTENSION vector;
```

## Quick Start

```python
from mem_vault import VectorMemory

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

### Adding Memories with Metadata

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
```

### Bulk Operations

```python
# Add multiple memories at once
memory.add_memories(
    conversation_id="user_123",
    contents=[
        "User opened dashboard",
        "User viewed reports",
        "User downloaded PDF"
    ],
    metadata_list=[
        {"action": "view", "page": "dashboard"},
        {"action": "view", "page": "reports"},
        {"action": "download", "type": "pdf"}
    ]
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
```

## Configuration

```python
memory = VectorMemory.initialize(
    host="localhost",
    port=5432,
    database="your_db",
    user="your_user",
    password="your_password",
    openai_api_key="your-openai-key",
    
    # Optional settings
    pool_size=5,              # Connection pool size
    max_overflow=10,          # Max additional connections
    max_tokens=8191,          # Maximum tokens per content
    embedding_model="text-embedding-ada-002"  # OpenAI embedding model
)
```

## Error Handling

```python
from mem_vault.exceptions import StorageError

try:
    memory.add_memory(
        conversation_id="user_123",
        content="Some content"
    )
except StorageError as e:
    print(f"Failed to store memory: {e}")
```

## Best Practices

1. Use descriptive conversation IDs
2. Include relevant metadata with timestamps
3. Implement regular cleanup of old conversations
4. Use appropriate similarity thresholds for retrieval
5. Use bulk operations for multiple memories
6. Enable connection pooling for high-traffic applications

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.