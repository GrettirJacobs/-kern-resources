"""
Layer 1: Exact Storage

This module implements Layer 1 of the memory system, which stores
exact duplicates of text, code, documents, and other content.
"""

import os
import uuid
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
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

logger = logging.getLogger("MemorySystem.Layer1")

class ExactStorage:
    """
    Layer 1: Exact Storage

    Stores exact duplicates of content with vector embeddings for retrieval.
    """

    def __init__(self, client: Optional[QdrantClient] = None):
        """
        Initialize the Exact Storage layer.

        Args:
            client: QdrantClient instance (optional)
        """
        self.collection_name = config.get("vector_db.collections.exact_storage.name", "exact_storage")
        self.vector_size = config.get("vector_db.collections.exact_storage.vector_size", 384)
        self.distance = config.get("vector_db.collections.exact_storage.distance", "cosine")

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
            # Create index for content_type
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="content_type",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            # Create index for source
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="source",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            # Create index for timestamp
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="timestamp",
                field_schema=models.PayloadSchemaType.DATETIME
            )

            # Create index for memory_id
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="memory_id",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            logger.info(f"Created payload indexes for collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Error creating payload indexes: {str(e)}")

    def store_memory(
        self,
        content: str,
        embedding: List[float],
        content_type: str = "text",
        source: str = "user",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a memory in the exact storage layer.

        Args:
            content: The content to store
            embedding: Vector embedding of the content
            content_type: Type of content (text, code, document, etc.)
            source: Source of the content
            metadata: Additional metadata

        Returns:
            memory_id: Unique identifier for the stored memory
        """
        try:
            # Generate a unique memory ID string (for the payload)
            memory_id_str = f"memory_{uuid.uuid4().hex}"

            # Generate a unique integer ID for Qdrant
            # Use the first 8 bytes of the UUID as an integer
            memory_id_int = int(uuid.uuid4().hex[:8], 16)

            # Create a hash of the content for deduplication
            content_hash = hashlib.md5(content.encode()).hexdigest()

            # Prepare the payload
            payload = {
                "memory_id": memory_id_str,  # Store the string ID in the payload
                "content": content,
                "content_hash": content_hash,
                "content_type": content_type,
                "source": source,
                "timestamp": datetime.now().isoformat(),
            }

            # Add metadata if provided
            if metadata:
                payload["metadata"] = metadata

            # Create the point with integer ID
            point = models.PointStruct(
                id=memory_id_int,  # Use integer ID for Qdrant
                vector=embedding,
                payload=payload
            )

            # Store the point
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            logger.info(f"Stored memory with ID: {memory_id_str} (internal ID: {memory_id_int})")
            return memory_id_str
        except Exception as e:
            logger.error(f"Error storing memory: {str(e)}")
            raise

    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a memory by its ID.

        Args:
            memory_id: The unique identifier of the memory (string ID)

        Returns:
            The memory data or None if not found
        """
        try:
            # Search for the memory by its string ID in the payload
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
                limit=1
            )

            # Unpack the tuple returned by scroll
            points, _ = search_result

            if not points:
                logger.warning(f"Memory with ID {memory_id} not found")
                return None

            # Extract the payload
            memory = points[0].payload

            logger.info(f"Retrieved memory with ID: {memory_id}")
            return memory
        except Exception as e:
            logger.error(f"Error retrieving memory: {str(e)}")
            raise

    def search_similar(
        self,
        embedding: List[float],
        limit: int = 10,
        content_type: Optional[str] = None,
        source: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar memories based on vector similarity.

        Args:
            embedding: Vector embedding to search for
            limit: Maximum number of results
            content_type: Filter by content type
            source: Filter by source
            start_date: Filter by start date (ISO format)
            end_date: Filter by end date (ISO format)

        Returns:
            List of similar memories
        """
        try:
            # Prepare filter conditions
            filter_conditions = []

            if content_type:
                filter_conditions.append(
                    models.FieldCondition(
                        key="content_type",
                        match=models.MatchValue(value=content_type)
                    )
                )

            if source:
                filter_conditions.append(
                    models.FieldCondition(
                        key="source",
                        match=models.MatchValue(value=source)
                    )
                )

            if start_date or end_date:
                range_condition = {}

                if start_date:
                    range_condition["gte"] = start_date

                if end_date:
                    range_condition["lte"] = end_date

                filter_conditions.append(
                    models.FieldCondition(
                        key="timestamp",
                        range=models.Range(**range_condition)
                    )
                )

            # Create the filter
            search_filter = None
            if filter_conditions:
                search_filter = models.Filter(
                    must=filter_conditions
                )

            # Search for similar vectors
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=embedding,
                query_filter=search_filter,
                limit=limit
            )

            # Extract the results
            results = []
            for point in search_result:
                memory = point.payload
                memory["score"] = point.score
                results.append(memory)

            logger.info(f"Found {len(results)} similar memories")
            return results
        except Exception as e:
            logger.error(f"Error searching similar memories: {str(e)}")
            raise

    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory by its ID.

        Args:
            memory_id: The unique identifier of the memory (string ID)

        Returns:
            True if the memory was deleted, False otherwise
        """
        try:
            # First, find the internal integer ID by searching for the string ID
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
                limit=1
            )

            # Unpack the tuple returned by scroll
            points, _ = search_result

            if not points:
                logger.warning(f"Memory with ID {memory_id} not found for deletion")
                return False

            # Get the internal integer ID
            internal_id = points[0].id

            # Delete the point using the internal ID
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[internal_id]
                )
            )

            logger.info(f"Deleted memory with ID: {memory_id} (internal ID: {internal_id})")
            return True
        except Exception as e:
            logger.error(f"Error deleting memory: {str(e)}")
            return False

    def get_all_memories(
        self,
        limit: int = 100,
        offset: Optional[str] = None,
        content_type: Optional[str] = None,
        source: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Get all memories with pagination.

        Args:
            limit: Maximum number of results
            offset: Pagination offset
            content_type: Filter by content type
            source: Filter by source

        Returns:
            Tuple of (list of memories, next offset)
        """
        try:
            # Prepare filter conditions
            filter_conditions = []

            if content_type:
                filter_conditions.append(
                    models.FieldCondition(
                        key="content_type",
                        match=models.MatchValue(value=content_type)
                    )
                )

            if source:
                filter_conditions.append(
                    models.FieldCondition(
                        key="source",
                        match=models.MatchValue(value=source)
                    )
                )

            # Create the filter
            scroll_filter = None
            if filter_conditions:
                scroll_filter = models.Filter(
                    must=filter_conditions
                )

            # Get all points
            scroll_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=scroll_filter,
                limit=limit,
                offset=offset
            )

            # Unpack the tuple returned by scroll
            points, next_offset = scroll_result

            # Extract the results
            results = [point.payload for point in points]

            logger.info(f"Retrieved {len(results)} memories")
            return results, next_offset
        except Exception as e:
            logger.error(f"Error retrieving all memories: {str(e)}")
            raise

    def count_memories(
        self,
        content_type: Optional[str] = None,
        source: Optional[str] = None
    ) -> int:
        """
        Count the number of memories.

        Args:
            content_type: Filter by content type
            source: Filter by source

        Returns:
            Number of memories
        """
        try:
            # Prepare filter conditions
            filter_conditions = []

            if content_type:
                filter_conditions.append(
                    models.FieldCondition(
                        key="content_type",
                        match=models.MatchValue(value=content_type)
                    )
                )

            if source:
                filter_conditions.append(
                    models.FieldCondition(
                        key="source",
                        match=models.MatchValue(value=source)
                    )
                )

            # Create the filter
            count_filter = None
            if filter_conditions:
                count_filter = models.Filter(
                    must=filter_conditions
                )

            # Count the points
            count_result = self.client.count(
                collection_name=self.collection_name,
                count_filter=count_filter
            )

            logger.info(f"Counted {count_result.count} memories")
            return count_result.count
        except Exception as e:
            logger.error(f"Error counting memories: {str(e)}")
            raise

    def check_duplicate(self, content: str) -> Optional[str]:
        """
        Check if a memory with the same content already exists.

        Args:
            content: The content to check

        Returns:
            The memory_id (string ID) of the duplicate if found, None otherwise
        """
        try:
            # Create a hash of the content
            content_hash = hashlib.md5(content.encode()).hexdigest()

            # Search for the hash
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="content_hash",
                            match=models.MatchValue(value=content_hash)
                        )
                    ]
                ),
                limit=1
            )

            # Unpack the tuple returned by scroll
            points, _ = search_result

            if points:
                # Get the string memory_id from the payload
                memory_id = points[0].payload.get("memory_id")
                logger.info(f"Found duplicate memory with ID: {memory_id}")
                return memory_id

            logger.info("No duplicate memory found")
            return None
        except Exception as e:
            logger.error(f"Error checking for duplicate: {str(e)}")
            raise
