"""
Layer 2: Machine-Readable Tags

This module implements Layer 2 of the memory system, which stores
machine-readable tags for each document.
"""

import os
import uuid
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple, Set
import logging
import numpy as np

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
except ImportError:
    raise ImportError(
        "Qdrant client not installed. Please install it with: pip install qdrant-client"
    )

from memory_system.config import config

logger = logging.getLogger("MemorySystem.Layer2")

class TagStorage:
    """
    Layer 2: Tag Storage

    Stores machine-readable tags for each memory with vector embeddings for retrieval.
    """

    def __init__(self, client: Optional[QdrantClient] = None):
        """
        Initialize the Tag Storage layer.

        Args:
            client: QdrantClient instance (optional)
        """
        self.collection_name = config.get("vector_db.collections.memory_tags.name", "memory_tags")
        self.vector_size = config.get("vector_db.collections.memory_tags.vector_size", 384)
        self.distance = config.get("vector_db.collections.memory_tags.distance", "cosine")

        # Connect to Qdrant
        if client:
            self.client = client
        else:
            host = config.get("vector_db.host", "localhost")
            port = config.get("vector_db.port", 6333)
            self.client = QdrantClient(host=host, port=port)

        # Ensure the collection exists
        self._ensure_collection_exists()

    def _ensure_collection_exists(self) -> None:
        """Ensure the collection exists in Qdrant."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                logger.info(f"Creating collection '{self.collection_name}'")

                # Convert string distance to enum
                distance_map = {
                    "cosine": models.Distance.COSINE,
                    "euclid": models.Distance.EUCLID,
                    "dot": models.Distance.DOT
                }
                distance = distance_map.get(self.distance.lower(), models.Distance.COSINE)

                # Create the collection
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=distance
                    )
                )

                # Create payload indexes for efficient filtering
                self._create_payload_indexes()

                logger.info(f"Collection '{self.collection_name}' created successfully")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {str(e)}")
            raise

    def _create_payload_indexes(self) -> None:
        """Create payload indexes for efficient filtering."""
        try:
            # Create index for memory_id
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="memory_id",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            # Create index for tag_type
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="tag_type",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            # Create index for tag_value
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="tag_value",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            # Create index for timestamp
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="timestamp",
                field_schema=models.PayloadSchemaType.DATETIME
            )

            logger.info(f"Created payload indexes for collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Error creating payload indexes: {str(e)}")

    def add_tags(
        self,
        memory_id: str,
        tags: List[Dict[str, Any]],
        embedding: Optional[List[float]] = None
    ) -> bool:
        """
        Add tags to a memory.

        Args:
            memory_id: The unique identifier of the memory (string ID)
            tags: List of tag dictionaries with 'type', 'value', and optional 'score'
            embedding: Vector embedding for the tags (optional)

        Returns:
            True if tags were added successfully, False otherwise
        """
        try:
            # Generate points for each tag
            points = []

            for i, tag in enumerate(tags):
                # Generate a unique tag ID string for the payload
                tag_id_str = f"{memory_id}_tag_{i}"

                # Generate a unique integer ID for Qdrant
                # Use the first 8 bytes of a UUID as an integer
                tag_id_int = int(uuid.uuid4().hex[:8], 16)

                # Prepare the payload
                payload = {
                    "memory_id": memory_id,  # String memory ID
                    "tag_id": tag_id_str,    # String tag ID
                    "tag_type": tag.get("type", "general"),
                    "tag_value": tag.get("value", ""),
                    "tag_score": tag.get("score", 1.0),
                    "timestamp": datetime.now().isoformat(),
                }

                # Add any additional fields from the tag
                for key, value in tag.items():
                    if key not in ["type", "value", "score"]:
                        payload[key] = value

                # Use the provided embedding or a default one
                tag_embedding = embedding if embedding else [0.0] * self.vector_size

                # Create the point with integer ID
                point = models.PointStruct(
                    id=tag_id_int,  # Use integer ID for Qdrant
                    vector=tag_embedding,
                    payload=payload
                )

                points.append(point)

            # Store the points
            if points:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )

                logger.info(f"Added {len(points)} tags to memory {memory_id}")
                return True
            else:
                logger.warning(f"No tags to add for memory {memory_id}")
                return False
        except Exception as e:
            logger.error(f"Error adding tags: {str(e)}")
            return False

    def get_tags(self, memory_id: str) -> List[Dict[str, Any]]:
        """
        Get all tags for a memory.

        Args:
            memory_id: The unique identifier of the memory

        Returns:
            List of tag dictionaries
        """
        try:
            # Search for tags with the memory_id
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="memory_id",
                            match=models.MatchValue(value=memory_id)
                        )
                    ]
                ),
                limit=100
            )

            # Unpack the tuple returned by scroll
            points, _ = search_result

            # Extract the tags
            tags = []
            for point in points:
                payload = point.payload
                tag = {
                    "type": payload.get("tag_type", "general"),
                    "value": payload.get("tag_value", ""),
                    "score": payload.get("tag_score", 1.0),
                }

                # Add any additional fields from the payload
                for key, value in payload.items():
                    if key not in ["memory_id", "tag_id", "tag_type", "tag_value", "tag_score", "timestamp"]:
                        tag[key] = value

                tags.append(tag)

            logger.info(f"Retrieved {len(tags)} tags for memory {memory_id}")
            return tags
        except Exception as e:
            logger.error(f"Error retrieving tags: {str(e)}")
            return []

    def search_by_tag(
        self,
        tag_type: Optional[str] = None,
        tag_value: Optional[str] = None,
        limit: int = 100
    ) -> List[str]:
        """
        Search for memories by tag.

        Args:
            tag_type: The type of tag to search for
            tag_value: The value of tag to search for
            limit: Maximum number of results

        Returns:
            List of memory IDs
        """
        try:
            # Prepare filter conditions
            filter_conditions = []

            if tag_type:
                filter_conditions.append(
                    models.FieldCondition(
                        key="tag_type",
                        match=models.MatchValue(value=tag_type)
                    )
                )

            if tag_value:
                filter_conditions.append(
                    models.FieldCondition(
                        key="tag_value",
                        match=models.MatchValue(value=tag_value)
                    )
                )

            # Create the filter
            scroll_filter = None
            if filter_conditions:
                scroll_filter = models.Filter(
                    must=filter_conditions
                )
            else:
                logger.warning("No tag filters specified")
                return []

            # Search for tags
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=scroll_filter,
                limit=limit
            )

            # Unpack the tuple returned by scroll
            points, _ = search_result

            # Extract unique memory IDs
            memory_ids = set()
            for point in points:
                memory_id = point.payload.get("memory_id")
                if memory_id:
                    memory_ids.add(memory_id)

            logger.info(f"Found {len(memory_ids)} memories with matching tags")
            return list(memory_ids)
        except Exception as e:
            logger.error(f"Error searching by tag: {str(e)}")
            return []

    def delete_tags(self, memory_id: str) -> bool:
        """
        Delete all tags for a memory.

        Args:
            memory_id: The unique identifier of the memory (string ID)

        Returns:
            True if tags were deleted successfully, False otherwise
        """
        try:
            # First, find all tag points with this memory_id
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="memory_id",
                            match=models.MatchValue(value=memory_id)
                        )
                    ]
                ),
                limit=100  # Assuming no more than 100 tags per memory
            )

            # Unpack the tuple returned by scroll
            points, _ = search_result

            if not points:
                logger.warning(f"No tags found for memory {memory_id}")
                return True  # No tags to delete is still a success

            # Get all internal integer IDs
            internal_ids = [point.id for point in points]

            # Delete the points using their internal IDs
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=internal_ids
                )
            )

            logger.info(f"Deleted {len(internal_ids)} tags for memory {memory_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting tags: {str(e)}")
            return False

    def get_all_tag_types(self) -> List[str]:
        """
        Get all unique tag types in the system.

        Returns:
            List of unique tag types
        """
        try:
            # This is a simplified approach - in a real system, you might want to
            # maintain a separate collection for tag types and values

            # Get all points
            all_tags = []
            offset = None

            while True:
                search_result = self.client.scroll(
                    collection_name=self.collection_name,
                    limit=1000,
                    offset=offset
                )

                # Unpack the tuple returned by scroll
                points, offset = search_result

                if not points:
                    break

                # Extract tag types
                for point in points:
                    tag_type = point.payload.get("tag_type")
                    if tag_type:
                        all_tags.append(tag_type)

                if not offset:
                    break

            # Get unique tag types
            unique_tags = list(set(all_tags))

            logger.info(f"Retrieved {len(unique_tags)} unique tag types")
            return unique_tags
        except Exception as e:
            logger.error(f"Error retrieving tag types: {str(e)}")
            return []

    def get_tag_values(self, tag_type: str) -> List[str]:
        """
        Get all unique values for a specific tag type.

        Args:
            tag_type: The type of tag

        Returns:
            List of unique tag values
        """
        try:
            # Search for tags with the specified type
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="tag_type",
                            match=models.MatchValue(value=tag_type)
                        )
                    ]
                ),
                limit=1000
            )

            # Unpack the tuple returned by scroll
            points, _ = search_result

            # Extract unique tag values
            tag_values = set()
            for point in points:
                tag_value = point.payload.get("tag_value")
                if tag_value:
                    tag_values.add(tag_value)

            logger.info(f"Retrieved {len(tag_values)} unique values for tag type '{tag_type}'")
            return list(tag_values)
        except Exception as e:
            logger.error(f"Error retrieving tag values: {str(e)}")
            return []

    def get_memories_with_all_tags(self, tags: List[Dict[str, str]]) -> List[str]:
        """
        Get memories that have all the specified tags.

        Args:
            tags: List of tag dictionaries with 'type' and 'value'

        Returns:
            List of memory IDs
        """
        try:
            if not tags:
                logger.warning("No tags specified")
                return []

            # Get memories for each tag
            tag_memory_sets = []

            for tag in tags:
                tag_type = tag.get("type")
                tag_value = tag.get("value")

                if not tag_type or not tag_value:
                    continue

                # Get memories with this tag
                memory_ids = self.search_by_tag(tag_type, tag_value)

                if memory_ids:
                    tag_memory_sets.append(set(memory_ids))

            if not tag_memory_sets:
                return []

            # Find intersection of all sets
            result_set = tag_memory_sets[0]
            for memory_set in tag_memory_sets[1:]:
                result_set = result_set.intersection(memory_set)

            logger.info(f"Found {len(result_set)} memories with all specified tags")
            return list(result_set)
        except Exception as e:
            logger.error(f"Error finding memories with all tags: {str(e)}")
            return []

    def get_memories_with_any_tag(self, tags: List[Dict[str, str]]) -> List[str]:
        """
        Get memories that have any of the specified tags.

        Args:
            tags: List of tag dictionaries with 'type' and 'value'

        Returns:
            List of memory IDs
        """
        try:
            if not tags:
                logger.warning("No tags specified")
                return []

            # Get memories for each tag
            all_memory_ids = set()

            for tag in tags:
                tag_type = tag.get("type")
                tag_value = tag.get("value")

                if not tag_type or not tag_value:
                    continue

                # Get memories with this tag
                memory_ids = self.search_by_tag(tag_type, tag_value)

                if memory_ids:
                    all_memory_ids.update(memory_ids)

            logger.info(f"Found {len(all_memory_ids)} memories with any of the specified tags")
            return list(all_memory_ids)
        except Exception as e:
            logger.error(f"Error finding memories with any tag: {str(e)}")
            return []

    def get_memories_with_tag(self, tag_type: Optional[str] = None, tag_value: Optional[str] = None, limit: int = 100) -> List[str]:
        """
        Get memories that have the specified tag.

        Args:
            tag_type: The type of tag (optional)
            tag_value: The value of tag (optional)
            limit: Maximum number of results

        Returns:
            List of memory IDs
        """
        try:
            # Use the existing search_by_tag method
            memory_ids = self.search_by_tag(tag_type, tag_value, limit)
            logger.info(f"Found {len(memory_ids)} memories with tag type '{tag_type}' and value '{tag_value}'")
            return memory_ids
        except Exception as e:
            logger.error(f"Error finding memories with tag: {str(e)}")
            return []

    def get_all_tags(self) -> List[Dict[str, Any]]:
        """
        Get all tags in the system.

        Returns:
            List of tag dictionaries with 'type' and 'value'
        """
        try:
            # Get all points
            all_tags = []
            offset = None

            while True:
                search_result = self.client.scroll(
                    collection_name=self.collection_name,
                    limit=1000,
                    offset=offset
                )

                # Unpack the tuple returned by scroll
                points, offset = search_result

                if not points:
                    break

                # Extract tags
                for point in points:
                    tag = {
                        "type": point.payload.get("tag_type", "general"),
                        "value": point.payload.get("tag_value", ""),
                        "score": point.payload.get("tag_score", 1.0),
                    }
                    all_tags.append(tag)

                if not offset:
                    break

            # Remove duplicates (same type and value)
            unique_tags = []
            seen = set()
            for tag in all_tags:
                key = (tag["type"], tag["value"])
                if key not in seen:
                    seen.add(key)
                    unique_tags.append(tag)

            logger.info(f"Retrieved {len(unique_tags)} unique tags")
            return unique_tags
        except Exception as e:
            logger.error(f"Error retrieving all tags: {str(e)}")
            return []
