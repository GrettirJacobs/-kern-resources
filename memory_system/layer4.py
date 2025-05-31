"""
Layer 4: Meta Commentaries

This module implements Layer 4 of the memory system, which generates
AI-created meta commentaries regarding groups of memories.

Currently uses Anthropic's Claude 3 for generating meta commentaries.
In the future, this will be implemented as an agent using Google's A2A protocol.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
import time
from datetime import datetime

try:
    import anthropic
except ImportError:
    raise ImportError(
        "Anthropic client not installed. Please install it with: pip install anthropic"
    )

from memory_system.config import config

logger = logging.getLogger("MemorySystem.Layer4")

class MetaCommentaryGenerator:
    """
    Layer 4: Meta Commentary Generator
    
    Generates AI meta commentaries regarding groups of memories.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Meta Commentary Generator.
        
        Args:
            api_key: Anthropic API key (optional, can be set in config or env var)
        """
        # Get API key from config, parameter, or environment variable
        self.api_key = api_key or config.get("anthropic.api_key") or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            logger.warning("No Anthropic API key provided. Layer 4 functionality will be limited.")
        
        # Set up Anthropic client
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            logger.info("Anthropic client initialized")
        else:
            self.client = None
        
        # Get model configuration
        self.model = config.get("anthropic.model", "claude-3-sonnet-20240229")
        self.temperature = config.get("anthropic.temperature", 0.7)
        self.max_tokens = config.get("anthropic.max_tokens", 1000)
        
        logger.info(f"Using Anthropic model: {self.model}")
    
    def generate_meta_commentary(
        self, 
        memories: List[Dict[str, Any]],
        commentary_type: str = "connections"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a meta commentary for a group of memories.
        
        Args:
            memories: List of memory data
            commentary_type: Type of commentary to generate (connections, patterns, implications)
            
        Returns:
            Meta commentary data or None if generation failed
        """
        if not self.client:
            logger.warning("Cannot generate meta commentary: No Anthropic client available")
            return self._generate_mock_meta_commentary(memories, commentary_type)
        
        try:
            # Extract memory contents and summaries
            memory_texts = []
            for i, memory in enumerate(memories):
                content = memory.get("content", "")
                tags = memory.get("tags", [])
                
                # Format tags
                tags_text = ""
                if tags:
                    tags_text = "Tags: " + ", ".join([f"{tag.get('type', 'general')}: {tag.get('value', '')}" for tag in tags])
                
                memory_texts.append(f"Memory {i+1}:\n{content}\n{tags_text}")
            
            # Join memory texts
            all_memories = "\n\n".join(memory_texts)
            
            # Create prompt based on commentary type
            if commentary_type == "patterns":
                prompt = f"Please analyze the following memories and identify patterns, trends, and recurring themes across them.\n\n{all_memories}"
            elif commentary_type == "implications":
                prompt = f"Please analyze the following memories and discuss their broader implications, potential applications, and future directions.\n\n{all_memories}"
            else:  # connections
                prompt = f"Please analyze the following memories and identify connections, relationships, and how they complement or contradict each other.\n\n{all_memories}"
            
            # Call Anthropic API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system="You are an expert analyst specializing in finding connections and patterns across different pieces of information. You provide insightful meta-level analysis.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract commentary text
            commentary_text = response.content[0].text
            
            # Create meta commentary data
            meta_commentary = {
                "memory_ids": [memory.get("memory_id") for memory in memories if memory.get("memory_id")],
                "commentary_type": commentary_type,
                "commentary_text": commentary_text,
                "model": self.model,
                "timestamp": datetime.now().isoformat(),
            }
            
            logger.info(f"Generated {commentary_type} meta commentary for {len(memories)} memories")
            return meta_commentary
        except Exception as e:
            logger.error(f"Error generating meta commentary: {str(e)}")
            return self._generate_mock_meta_commentary(memories, commentary_type)
    
    def _generate_mock_meta_commentary(
        self, 
        memories: List[Dict[str, Any]],
        commentary_type: str
    ) -> Dict[str, Any]:
        """
        Generate a mock meta commentary when API is not available.
        
        Args:
            memories: List of memory data
            commentary_type: Type of commentary to generate
            
        Returns:
            Mock meta commentary data
        """
        logger.warning(f"Generating mock {commentary_type} meta commentary for {len(memories)} memories")
        
        if commentary_type == "patterns":
            commentary_text = f"Pattern Analysis (Mock): These {len(memories)} memories show recurring themes related to their content domains."
        elif commentary_type == "implications":
            commentary_text = f"Implications Analysis (Mock): The {len(memories)} memories suggest potential applications in their respective domains."
        else:  # connections
            commentary_text = f"Connections Analysis (Mock): The {len(memories)} memories are connected through their shared concepts and technologies."
        
        return {
            "memory_ids": [memory.get("memory_id") for memory in memories if memory.get("memory_id")],
            "commentary_type": commentary_type,
            "commentary_text": commentary_text,
            "model": "mock",
            "timestamp": datetime.now().isoformat(),
        }
    
    def generate_multiple_commentaries(
        self, 
        memories: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Generate multiple types of meta commentaries for a group of memories.
        
        Args:
            memories: List of memory data
            
        Returns:
            Dictionary of commentary types and their data
        """
        commentary_types = ["connections", "patterns", "implications"]
        commentaries = {}
        
        for commentary_type in commentary_types:
            commentary = self.generate_meta_commentary(memories, commentary_type)
            if commentary:
                commentaries[commentary_type] = commentary
        
        logger.info(f"Generated {len(commentaries)} meta commentaries for {len(memories)} memories")
        return commentaries
    
    def analyze_relationship(
        self, 
        memory1: Dict[str, Any],
        memory2: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze the relationship between two memories.
        
        Args:
            memory1: First memory data
            memory2: Second memory data
            
        Returns:
            Relationship analysis data or None if analysis failed
        """
        if not self.client:
            logger.warning("Cannot analyze relationship: No Anthropic client available")
            return None
        
        try:
            # Extract memory contents
            content1 = memory1.get("content", "")
            content2 = memory2.get("content", "")
            
            # Create prompt
            prompt = f"""Please analyze the relationship between these two pieces of information:

Memory 1:
{content1}

Memory 2:
{content2}

Analyze how they relate to each other, including:
1. Similarities and differences
2. How they complement each other
3. Any contradictions or tensions
4. How understanding one enhances understanding of the other
"""
            
            # Call Anthropic API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system="You are an expert analyst specializing in comparing and contrasting different pieces of information. You provide insightful relationship analysis.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract analysis text
            analysis_text = response.content[0].text
            
            # Create relationship analysis data
            analysis = {
                "memory_id1": memory1.get("memory_id"),
                "memory_id2": memory2.get("memory_id"),
                "analysis_text": analysis_text,
                "model": self.model,
                "timestamp": datetime.now().isoformat(),
            }
            
            logger.info(f"Generated relationship analysis between memories {memory1.get('memory_id')} and {memory2.get('memory_id')}")
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing relationship: {str(e)}")
            return None
    
    def suggest_new_connections(
        self, 
        memory: Dict[str, Any],
        all_memories: List[Dict[str, Any]],
        max_connections: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Suggest new connections between a memory and other memories.
        
        Args:
            memory: The target memory data
            all_memories: List of all available memories
            max_connections: Maximum number of connections to suggest
            
        Returns:
            List of suggested connections
        """
        if not self.client:
            logger.warning("Cannot suggest connections: No Anthropic client available")
            return []
        
        try:
            # Extract memory content
            memory_id = memory.get("memory_id")
            content = memory.get("content", "")
            
            # Filter out the target memory from all_memories
            other_memories = [m for m in all_memories if m.get("memory_id") != memory_id]
            
            # Limit the number of memories to consider
            other_memories = other_memories[:10]  # Consider at most 10 other memories
            
            # Create memory descriptions
            memory_descriptions = []
            for i, m in enumerate(other_memories):
                m_id = m.get("memory_id")
                m_content = m.get("content", "")
                memory_descriptions.append(f"Memory {i+1} (ID: {m_id}):\n{m_content[:200]}...")
            
            # Join memory descriptions
            all_descriptions = "\n\n".join(memory_descriptions)
            
            # Create prompt
            prompt = f"""I have a target memory and several other memories. Please suggest up to {max_connections} other memories that might have meaningful connections with the target memory.

Target Memory:
{content}

Other Memories:
{all_descriptions}

For each suggested connection, provide:
1. The ID of the connected memory
2. A brief explanation of why they are connected
3. A score from 0.0 to 1.0 indicating the strength of the connection

Format your response as a JSON array:
[
  {{"memory_id": "memory_123", "explanation": "These are connected because...", "score": 0.85}},
  ...
]
"""
            
            # Call Anthropic API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.3,  # Lower temperature for more consistent output
                system="You are an expert at finding connections between different pieces of information. You provide insightful connection suggestions in the exact format requested.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract connections text
            connections_text = response.content[0].text
            
            # Parse JSON
            try:
                # Find JSON array in the response
                start_idx = connections_text.find("[")
                end_idx = connections_text.rfind("]") + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = connections_text[start_idx:end_idx]
                    connections = json.loads(json_str)
                else:
                    # Fallback if JSON array not found
                    connections = []
            except json.JSONDecodeError:
                logger.warning("Failed to parse connections JSON, using empty list")
                connections = []
            
            logger.info(f"Generated {len(connections)} suggested connections for memory {memory_id}")
            return connections
        except Exception as e:
            logger.error(f"Error suggesting connections: {str(e)}")
            return []

# FUTURE DEVELOPMENT NOTE:
# In the future, this module will be replaced with an agent-based implementation
# using Google's Agent-to-Agent (A2A) protocol. The agent will be responsible for:
# 1. Generating meta commentaries about groups of memories
# 2. Analyzing relationships between memories
# 3. Suggesting new connections between memories
# 4. Communicating with other agents in the system
#
# The agent will be part of a team of specialized AI agents, each with different
# capabilities and responsibilities. This will enable more sophisticated and
# contextual memory processing.
