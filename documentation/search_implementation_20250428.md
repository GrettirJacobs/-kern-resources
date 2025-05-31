# Search Implementation

**Date**: April 28, 2025  
**Focus**: Implementing search functionality for the memory system

## 1. Overview

This document describes the implementation of search functionality for the Kern Resources memory system. The search functionality includes three types of search:

1. **Simple text search**: Basic keyword matching
2. **Vector search**: Semantic search using embeddings
3. **Tag search**: Structured search using metadata tags
4. **Dual search**: Combined approach using both vectors and tags

## 2. Components Implemented

### 2.1 Vector Search

Vector search uses embeddings to find semantically similar memories. It is implemented in the `search_vector` method of the `MemorySystem` class, which uses the existing `VectorSearch` class from the `creative_lab.memory_system` package.

Key features:
- Uses sentence transformers for embedding generation
- Uses FAISS for efficient similarity search
- Supports filtering by similarity threshold
- Returns full memory objects with similarity scores

### 2.2 Tag Search

Tag search uses metadata tags to find memories with specific tags. It is implemented in the `search_by_tag` method of the `MemorySystem` class, which has been updated to support tag queries in the format "tag:value".

Key features:
- Supports simple tag names and "tag:value" format
- Returns exact matches with relevance score of 1.0
- Sorts results by recency

### 2.3 Dual Search

Dual search combines vector search and tag search to provide more comprehensive results. It is implemented in the `search_dual` method of the `MemorySystem` class, which uses the new `DualSearch` class from the `kern_resources.core.memory.dual_search` module.

Key features:
- Performs vector search and tag search in parallel
- Combines results with configurable weights
- Extracts potential tags from natural language queries
- Returns combined results with detailed scoring information

## 3. Implementation Details

### 3.1 Memory System Updates

The `MemorySystem` class has been updated with the following methods:

```python
def search_vector(self, query: str, limit: int = 10, threshold: float = 0.5) -> List[Dict[str, Any]]:
    """
    Search for memories using vector embeddings.
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        threshold: Minimum similarity score to include in results
        
    Returns:
        List of dictionaries with memory content, metadata, and similarity scores
    """
    # Implementation details...
```

```python
def search_by_tag(self, tag_query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search for memories with a specific tag.

    Args:
        tag_query: Tag to search for (can be a simple tag name or in the format "tag:value")
        limit: Maximum number of results to return

    Returns:
        List of dictionaries with memory content and metadata
    """
    # Implementation details...
```

```python
def search_dual(
    self,
    query: str,
    limit: int = 10,
    vector_weight: float = 0.5,
    tag_weight: float = 0.5,
    threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Search for memories using both vector embeddings and tags.
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        vector_weight: Weight to give to vector search results (0.0 to 1.0)
        tag_weight: Weight to give to tag search results (0.0 to 1.0)
        threshold: Minimum similarity score to include in results
        
    Returns:
        Dictionary containing search results and metadata
    """
    # Implementation details...
```

### 3.2 Dual Search Class

A new `DualSearch` class has been created in the `kern_resources.core.memory.dual_search` module:

```python
class DualSearch:
    """
    Dual search system that combines vector embeddings and relational tags.
    
    This system performs two parallel searches:
    1. Vector-based semantic search using embeddings
    2. Tag-based relational search
    
    The results are then combined and ranked to provide more comprehensive results.
    """
    
    def __init__(
        self,
        memory_system: MemorySystem,
        vector_weight: float = 0.5,
        tag_weight: float = 0.5
    ):
        """
        Initialize the dual search system.
        
        Args:
            memory_system: The memory system to search
            vector_weight: Weight to give to vector search results (0.0 to 1.0)
            tag_weight: Weight to give to tag search results (0.0 to 1.0)
        """
        # Implementation details...
    
    def extract_tags_from_query(self, query: str) -> List[str]:
        """
        Extract potential tags from a natural language query.
        
        Args:
            query: The natural language query
            
        Returns:
            List of potential tags extracted from the query
        """
        # Implementation details...
    
    def search(
        self,
        query: str,
        limit: int = 10,
        vector_weight: Optional[float] = None,
        tag_weight: Optional[float] = None,
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Perform a dual search using both vector embeddings and relational tags.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            vector_weight: Weight to give to vector search results (0.0 to 1.0)
            tag_weight: Weight to give to tag search results (0.0 to 1.0)
            threshold: Minimum similarity score to include in results
            
        Returns:
            Dictionary containing search results and metadata
        """
        # Implementation details...
```

## 4. Testing

A comprehensive test script (`test_search.py`) has been created to verify the implementation. The test script includes:

- Testing simple text search
- Testing vector search
- Testing tag search
- Testing dual search

A script to add test memories (`add_test_memories.py`) has also been created to populate the memory system with test data for testing the search functionality.

All tests have passed, confirming that the implementation is working correctly.

## 5. Usage Examples

### 5.1 Simple Text Search

```python
from kern_resources.core.memory.memory_system import MemorySystem

# Create a memory system
memory_system = MemorySystem()

# Perform simple text search
results = memory_system.search("memory system", limit=5)

# Print results
for result in results:
    print(f"ID: {result.get('id')}")
    print(f"Content: {result.get('content')[:100]}...")
    print(f"Metadata: {result.get('metadata')}")
    print()
```

### 5.2 Vector Search

```python
# Perform vector search
results = memory_system.search_vector("memory system architecture", limit=5, threshold=0.7)

# Print results
for result in results:
    print(f"ID: {result.get('id')}")
    print(f"Similarity: {result.get('similarity')}")
    print(f"Content: {result.get('content')[:100]}...")
    print(f"Metadata: {result.get('metadata')}")
    print()
```

### 5.3 Tag Search

```python
# Perform tag search
results = memory_system.search_by_tag("tag:memory_system", limit=5)

# Print results
for result in results:
    print(f"ID: {result.get('id')}")
    print(f"Relevance: {result.get('relevance')}")
    print(f"Content: {result.get('content')[:100]}...")
    print(f"Metadata: {result.get('metadata')}")
    print()
```

### 5.4 Dual Search

```python
# Perform dual search
results = memory_system.search_dual(
    "memory system architecture",
    limit=5,
    vector_weight=0.6,
    tag_weight=0.4,
    threshold=0.5
)

# Print results
for result in results.get('results', []):
    print(f"ID: {result.get('id')}")
    print(f"Vector score: {result.get('vector_score')}")
    print(f"Tag score: {result.get('tag_score')}")
    print(f"Combined score: {result.get('combined_score')}")
    print(f"Content: {result.get('content')[:100]}...")
    print(f"Metadata: {result.get('metadata')}")
    print()
```

## 6. Conclusion

The implementation of search functionality enhances the memory system by providing multiple ways to search for memories. The combination of vector search and tag search in the dual search functionality provides a comprehensive search capability that can find memories based on both semantic similarity and structured metadata.

The implementation is flexible, supporting different search types and configurable parameters. It has been thoroughly tested and is ready for use in the Kern Resources project.
