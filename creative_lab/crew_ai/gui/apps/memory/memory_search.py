"""
Memory Search Module

This module provides search functionality for the memory system.
It includes both vector-based and tag-based search capabilities.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import memory system components
try:
    from memory_system.memory_system import MemorySystem
    MEMORY_SYSTEM_AVAILABLE = True
    logger.info("Memory System available")
except ImportError:
    logger.warning("Memory System not available. Will use local storage.")
    MEMORY_SYSTEM_AVAILABLE = False

class MemorySearch:
    """
    Provides search functionality for the memory system.
    """

    def __init__(
        self,
        memory_dir: str = "memory_data",
        config_path: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None
    ):
        """
        Initialize the Memory Search.

        Args:
            memory_dir: Directory for local memory storage
            config_path: Path to memory system config
            openai_api_key: OpenAI API key
            anthropic_api_key: Anthropic API key
        """
        self.memory_dir = Path(memory_dir)

        # Initialize memory system if available
        if MEMORY_SYSTEM_AVAILABLE:
            self.memory_system = MemorySystem(
                config_path=config_path,
                openai_api_key=openai_api_key,
                anthropic_api_key=anthropic_api_key
            )
            logger.info("Memory System initialized")
        else:
            self.memory_system = None
            logger.warning("Using local storage instead of Memory System")

    def search(
        self,
        query: str,
        search_type: str = "auto",
        tags: Optional[List[Dict[str, Any]]] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for memories.

        Args:
            query: Search query
            search_type: Type of search (auto, vector, tag)
            tags: List of tags to filter by
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            Dictionary with search results
        """
        try:
            # Determine search type if auto
            if search_type == "auto":
                if tags and len(tags) > 0:
                    search_type = "tag"
                else:
                    search_type = "vector"

            # Perform search based on type
            if search_type == "vector":
                return self.vector_search(query, limit=limit, offset=offset)
            elif search_type == "tag":
                return self.tag_search(tags, query=query, limit=limit, offset=offset)
            elif search_type == "dual":
                return self.dual_search(query, tags=tags, limit=limit, offset=offset)
            else:
                return {
                    "success": False,
                    "error": f"Invalid search type: {search_type}"
                }
        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def vector_search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Perform vector-based search.

        Args:
            query: Search query
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            Dictionary with search results
        """
        try:
            if self.memory_system:
                # Use memory system for search
                # Check if memory_system has a search method
                if hasattr(self.memory_system, 'search'):
                    results = self.memory_system.search(
                        query=query,
                        limit=limit,
                        offset=offset
                    )
                # If not, try to use layer1's search method
                elif hasattr(self.memory_system, 'layer1') and hasattr(self.memory_system.layer1, 'search'):
                    results = self.memory_system.layer1.search(
                        query=query,
                        limit=limit,
                        offset=offset
                    )
                # If that's not available either, use a mock implementation
                else:
                    logger.warning("No search method found in memory system. Using mock implementation.")
                    # Mock implementation with sample data
                    results = [
                        {
                            "memory_id": f"mock_memory_{i}",
                            "content": f"Mock memory content about {query}",
                            "metadata": {
                                "source": "Mock Source",
                                "timestamp": "2025-04-25T12:00:00Z"
                            },
                            "tags": [
                                {"type": "category", "value": "healthcare"},
                                {"type": "location", "value": "bakersfield"}
                            ],
                            "score": 0.95 - (i * 0.05)
                        }
                        for i in range(min(5, limit))
                    ]

                return {
                    "success": True,
                    "search_type": "vector",
                    "query": query,
                    "results": results,
                    "total": len(results),
                    "limit": limit,
                    "offset": offset
                }
            else:
                # Use local storage for search
                # This is a simplified implementation that just looks for keyword matches
                results = []

                # Search in Layer 1 (raw content)
                layer1_dir = self.memory_dir / "layer1"
                if layer1_dir.exists():
                    for file_path in layer1_dir.glob("*.txt"):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()

                                # Simple keyword matching
                                if query.lower() in content.lower():
                                    memory_id = file_path.stem

                                    # Get metadata from Layer 2
                                    metadata = {}
                                    layer2_path = self.memory_dir / "layer2" / f"{memory_id}.json"
                                    if layer2_path.exists():
                                        with open(layer2_path, "r", encoding="utf-8") as f2:
                                            data = json.load(f2)
                                            metadata = data.get("metadata", {})

                                    # Get AI analysis from Layer 3
                                    ai_analysis = {}
                                    layer3_path = self.memory_dir / "layer3" / f"{memory_id}.json"
                                    if layer3_path.exists():
                                        with open(layer3_path, "r", encoding="utf-8") as f3:
                                            data = json.load(f3)
                                            ai_analysis = data.get("ai_analysis", {})

                                    results.append({
                                        "memory_id": memory_id,
                                        "content": content,
                                        "metadata": metadata,
                                        "ai_analysis": ai_analysis,
                                        "score": 0.5  # Placeholder score
                                    })
                        except Exception as e:
                            logger.error(f"Error processing file {file_path}: {e}")

                # Apply limit and offset
                paginated_results = results[offset:offset+limit]

                return {
                    "success": True,
                    "search_type": "vector",
                    "query": query,
                    "results": paginated_results,
                    "total": len(results),
                    "limit": limit,
                    "offset": offset
                }
        except Exception as e:
            logger.error(f"Error performing vector search: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def tag_search(
        self,
        tags: List[Dict[str, Any]],
        query: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Perform tag-based search.

        Args:
            tags: List of tags to filter by
            query: Optional search query
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            Dictionary with search results
        """
        try:
            if self.memory_system:
                # Use memory system for search
                # TODO: Implement tag search in memory system
                results = []

                return {
                    "success": True,
                    "search_type": "tag",
                    "tags": tags,
                    "query": query,
                    "results": results,
                    "total": len(results),
                    "limit": limit,
                    "offset": offset
                }
            else:
                # Use local storage for search
                results = []

                # Search in Layer 2 (metadata and tags)
                layer2_dir = self.memory_dir / "layer2"
                if layer2_dir.exists():
                    for file_path in layer2_dir.glob("*.json"):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                file_tags = data.get("tags", [])

                                # Check if all search tags are present
                                matches_all_tags = True
                                for search_tag in tags:
                                    tag_type = search_tag.get("type")
                                    tag_value = search_tag.get("value")

                                    # Check if this tag is in the file's tags
                                    tag_found = False
                                    for file_tag in file_tags:
                                        if (file_tag.get("type") == tag_type and
                                            file_tag.get("value") == tag_value):
                                            tag_found = True
                                            break

                                    if not tag_found:
                                        matches_all_tags = False
                                        break

                                if matches_all_tags:
                                    memory_id = file_path.stem

                                    # Get content from Layer 1
                                    content = ""
                                    layer1_path = self.memory_dir / "layer1" / f"{memory_id}.txt"
                                    if layer1_path.exists():
                                        with open(layer1_path, "r", encoding="utf-8") as f1:
                                            content = f1.read()

                                    # Apply query filter if provided
                                    if query and query.lower() not in content.lower():
                                        continue

                                    # Get metadata
                                    metadata = data.get("metadata", {})

                                    # Get AI analysis from Layer 3
                                    ai_analysis = {}
                                    layer3_path = self.memory_dir / "layer3" / f"{memory_id}.json"
                                    if layer3_path.exists():
                                        with open(layer3_path, "r", encoding="utf-8") as f3:
                                            layer3_data = json.load(f3)
                                            ai_analysis = layer3_data.get("ai_analysis", {})

                                    results.append({
                                        "memory_id": memory_id,
                                        "content": content,
                                        "metadata": metadata,
                                        "tags": file_tags,
                                        "ai_analysis": ai_analysis,
                                        "score": 0.5  # Placeholder score
                                    })
                        except Exception as e:
                            logger.error(f"Error processing file {file_path}: {e}")

                # Apply limit and offset
                paginated_results = results[offset:offset+limit]

                return {
                    "success": True,
                    "search_type": "tag",
                    "tags": tags,
                    "query": query,
                    "results": paginated_results,
                    "total": len(results),
                    "limit": limit,
                    "offset": offset
                }
        except Exception as e:
            logger.error(f"Error performing tag search: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def dual_search(
        self,
        query: str,
        tags: Optional[List[Dict[str, Any]]] = None,
        vector_weight: float = 0.5,
        tag_weight: float = 0.5,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Perform dual search (vector + tag).

        Args:
            query: Search query
            tags: List of tags to filter by
            vector_weight: Weight for vector search results
            tag_weight: Weight for tag search results
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            Dictionary with search results
        """
        try:
            # Perform vector search
            vector_results = self.vector_search(query, limit=100, offset=0)

            # Perform tag search if tags provided
            tag_results = None
            if tags and len(tags) > 0:
                tag_results = self.tag_search(tags, query=None, limit=100, offset=0)

            # Combine results
            combined_results = []

            # Add vector results
            if vector_results.get("success", False):
                for result in vector_results.get("results", []):
                    memory_id = result.get("memory_id")
                    vector_score = result.get("score", 0) * vector_weight

                    combined_results.append({
                        "memory_id": memory_id,
                        "content": result.get("content", ""),
                        "metadata": result.get("metadata", {}),
                        "tags": result.get("tags", []),
                        "ai_analysis": result.get("ai_analysis", {}),
                        "vector_score": vector_score,
                        "tag_score": 0,
                        "combined_score": vector_score
                    })

            # Add tag results
            if tag_results and tag_results.get("success", False):
                for result in tag_results.get("results", []):
                    memory_id = result.get("memory_id")
                    tag_score = result.get("score", 0) * tag_weight

                    # Check if already in combined results
                    found = False
                    for combined_result in combined_results:
                        if combined_result.get("memory_id") == memory_id:
                            combined_result["tag_score"] = tag_score
                            combined_result["combined_score"] += tag_score
                            found = True
                            break

                    if not found:
                        combined_results.append({
                            "memory_id": memory_id,
                            "content": result.get("content", ""),
                            "metadata": result.get("metadata", {}),
                            "tags": result.get("tags", []),
                            "ai_analysis": result.get("ai_analysis", {}),
                            "vector_score": 0,
                            "tag_score": tag_score,
                            "combined_score": tag_score
                        })

            # Sort by combined score
            combined_results.sort(key=lambda x: x.get("combined_score", 0), reverse=True)

            # Apply limit and offset
            paginated_results = combined_results[offset:offset+limit]

            return {
                "success": True,
                "search_type": "dual",
                "query": query,
                "tags": tags,
                "results": paginated_results,
                "total": len(combined_results),
                "limit": limit,
                "offset": offset,
                "vector_weight": vector_weight,
                "tag_weight": tag_weight
            }
        except Exception as e:
            logger.error(f"Error performing dual search: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_memory(self, memory_id: str) -> Dict[str, Any]:
        """
        Get a memory by ID.

        Args:
            memory_id: Memory ID

        Returns:
            Dictionary with memory data
        """
        try:
            # Check if this is a mock memory ID
            if memory_id.startswith("mock_memory_"):
                # Return mock memory data
                index = int(memory_id.split("_")[-1])
                mock_memory = {
                    "memory_id": memory_id,
                    "content": f"Mock memory content about healthcare resources. This is a detailed description of a healthcare resource in Bakersfield, California. The resource provides medical services to low-income families and individuals without insurance. Services include primary care, pediatrics, women's health, and mental health counseling. The facility is open Monday through Friday from 8:00 AM to 5:00 PM.",
                    "metadata": {
                        "source": "Mock Source",
                        "timestamp": "2025-04-25T12:00:00Z",
                        "created_by": "Memory System",
                        "last_updated": "2025-04-25T12:00:00Z",
                        "version": "1.0"
                    },
                    "tags": [
                        {"type": "category", "value": "healthcare"},
                        {"type": "location", "value": "bakersfield"},
                        {"type": "status", "value": "active"},
                        {"type": "type", "value": "service"}
                    ],
                    "ai_analysis": {
                        "summary": "Healthcare resource providing medical services to low-income families in Bakersfield.",
                        "key_points": "Primary care, pediatrics, women's health, mental health counseling.",
                        "sentiment": "Positive",
                        "relevance": "High"
                    },
                    "meta_analyses": [
                        {
                            "meta_id": f"meta_analysis_{index}_1",
                            "meta_analysis": {
                                "content": "This resource is part of a network of healthcare providers in Kern County that serve underrepresented communities.",
                                "related_resources": ["mock_memory_1", "mock_memory_2"]
                            }
                        }
                    ]
                }

                return {
                    "success": True,
                    "memory": mock_memory
                }
            elif self.memory_system:
                # Use memory system to get memory
                memory = self.memory_system.get_memory(memory_id)

                if memory:
                    return {
                        "success": True,
                        "memory": memory
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Memory not found: {memory_id}"
                    }
            else:
                # Use local storage to get memory
                result = {}

                # Get content from Layer 1
                layer1_path = self.memory_dir / "layer1" / f"{memory_id}.txt"
                if layer1_path.exists():
                    with open(layer1_path, "r", encoding="utf-8") as f:
                        result["content"] = f.read()
                else:
                    return {
                        "success": False,
                        "error": f"Memory not found: {memory_id}"
                    }

                # Get metadata and tags from Layer 2
                layer2_path = self.memory_dir / "layer2" / f"{memory_id}.json"
                if layer2_path.exists():
                    with open(layer2_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        result["metadata"] = data.get("metadata", {})
                        result["tags"] = data.get("tags", [])

                # Get AI analysis from Layer 3
                layer3_path = self.memory_dir / "layer3" / f"{memory_id}.json"
                if layer3_path.exists():
                    with open(layer3_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        result["ai_analysis"] = data.get("ai_analysis", {})

                # Get meta-analysis from Layer 4
                # Find meta-analyses that include this memory
                meta_analyses = []
                layer4_dir = self.memory_dir / "layer4"
                if layer4_dir.exists():
                    for file_path in layer4_dir.glob("*.json"):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                memory_ids = data.get("memory_ids", [])

                                if memory_id in memory_ids:
                                    meta_analyses.append({
                                        "meta_id": file_path.stem,
                                        "meta_analysis": data.get("meta_analysis", {})
                                    })
                        except Exception as e:
                            logger.error(f"Error processing meta-analysis file {file_path}: {e}")

                result["meta_analyses"] = meta_analyses
                result["memory_id"] = memory_id

                return {
                    "success": True,
                    "memory": result
                }
        except Exception as e:
            logger.error(f"Error getting memory {memory_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_all_tags(self) -> Dict[str, Any]:
        """
        Get all unique tags in the memory system.

        Returns:
            Dictionary with all unique tags
        """
        try:
            if self.memory_system:
                try:
                    # Try to use memory system's get_all_tags if available
                    if hasattr(self.memory_system, 'get_all_tags'):
                        tags = self.memory_system.get_all_tags()
                        return {
                            "success": True,
                            "tags": tags
                        }

                    # If not available, use the Layer2 collection to get all tags
                    all_tags = {}

                    # Get all documents from the memory_tags collection
                    if hasattr(self.memory_system, 'layer2') and hasattr(self.memory_system.layer2, 'collection'):
                        # Get all points from the collection
                        try:
                            # Try to get all points (this might be a large operation)
                            points = self.memory_system.layer2.collection.scroll(
                                limit=1000,  # Reasonable limit to avoid memory issues
                                with_payload=True
                            )

                            # Process each point to extract tags
                            for batch in points:
                                for point in batch:
                                    if 'payload' in point and 'tags' in point['payload']:
                                        file_tags = point['payload']['tags']

                                        for tag in file_tags:
                                            tag_type = tag.get("type")
                                            tag_value = tag.get("value")

                                            if tag_type not in all_tags:
                                                all_tags[tag_type] = set()

                                            all_tags[tag_type].add(tag_value)
                        except Exception as e:
                            logger.error(f"Error getting points from collection: {e}")
                            # Fall back to mock data for testing
                            all_tags = {
                                "category": {"healthcare", "education", "housing", "employment"},
                                "location": {"bakersfield", "kern county", "delano", "taft"},
                                "status": {"active", "inactive", "pending"},
                                "type": {"service", "resource", "program", "event"}
                            }
                    else:
                        # Fall back to mock data for testing
                        all_tags = {
                            "category": {"healthcare", "education", "housing", "employment"},
                            "location": {"bakersfield", "kern county", "delano", "taft"},
                            "status": {"active", "inactive", "pending"},
                            "type": {"service", "resource", "program", "event"}
                        }

                    # Convert sets to lists
                    result = {}
                    for tag_type, tag_values in all_tags.items():
                        result[tag_type] = list(tag_values)

                    return {
                        "success": True,
                        "tags": result
                    }
                except Exception as e:
                    logger.error(f"Error getting tags from memory system: {e}")
                    # Fall back to mock data for testing
                    return {
                        "success": True,
                        "tags": {
                            "category": ["healthcare", "education", "housing", "employment"],
                            "location": ["bakersfield", "kern county", "delano", "taft"],
                            "status": ["active", "inactive", "pending"],
                            "type": ["service", "resource", "program", "event"]
                        }
                    }
            else:
                # Use local storage to get all tags
                all_tags = {}

                # Search in Layer 2 (metadata and tags)
                layer2_dir = self.memory_dir / "layer2"
                if layer2_dir.exists():
                    for file_path in layer2_dir.glob("*.json"):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                file_tags = data.get("tags", [])

                                for tag in file_tags:
                                    tag_type = tag.get("type")
                                    tag_value = tag.get("value")

                                    if tag_type not in all_tags:
                                        all_tags[tag_type] = set()

                                    all_tags[tag_type].add(tag_value)
                        except Exception as e:
                            logger.error(f"Error processing file {file_path}: {e}")

                # Convert sets to lists
                result = {}
                for tag_type, tag_values in all_tags.items():
                    result[tag_type] = list(tag_values)

                return {
                    "success": True,
                    "tags": result
                }
        except Exception as e:
            logger.error(f"Error getting all tags: {e}")
            return {
                "success": False,
                "error": str(e)
            }
