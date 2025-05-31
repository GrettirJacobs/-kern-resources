"""
Layer 3: AI Summaries

This module implements Layer 3 of the memory system, which generates
AI-created summaries, explanations, and commentaries about each tagged memory.

Currently uses OpenAI's GPT-3 for generating summaries.
In the future, this will be implemented as an agent using Google's A2A protocol.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
import time
from datetime import datetime

try:
    import openai
except ImportError:
    raise ImportError(
        "OpenAI client not installed. Please install it with: pip install openai"
    )

from memory_system.config import config

logger = logging.getLogger("MemorySystem.Layer3")

class SummaryGenerator:
    """
    Layer 3: Summary Generator

    Generates AI summaries, explanations, and commentaries about memories.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Summary Generator.

        Args:
            api_key: OpenAI API key (optional, can be set in config or env var)
        """
        # Get API key from config, parameter, or environment variable
        self.api_key = api_key or config.get("openai.api_key") or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            logger.warning("No OpenAI API key provided. Layer 3 functionality will be limited.")

        # Set up OpenAI client
        if self.api_key:
            # The client will be created when needed
            logger.info("OpenAI API key provided")
        else:
            logger.warning("No OpenAI API key provided - Layer 3 will use mock responses")

        # Get model configuration
        self.model = config.get("openai.model", "gpt-3.5-turbo")
        self.temperature = config.get("openai.temperature", 0.7)
        self.max_tokens = config.get("openai.max_tokens", 500)

        logger.info(f"Using OpenAI model: {self.model}")

    def generate_summary(
        self,
        memory: Dict[str, Any],
        summary_type: str = "general"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a summary for a memory.

        Args:
            memory: The memory data
            summary_type: Type of summary to generate (general, technical, conceptual)

        Returns:
            Summary data or None if generation failed
        """
        if not self.api_key:
            logger.warning("Cannot generate summary: No OpenAI API key provided")
            return self._generate_mock_summary(memory, summary_type)

        try:
            # Extract memory content and tags
            content = memory.get("content", "")
            tags = memory.get("tags", [])

            # Format tags for the prompt
            tags_text = ""
            if tags:
                tags_text = "Tags:\n" + "\n".join([f"- {tag.get('type', 'general')}: {tag.get('value', '')}" for tag in tags])

            # Create prompt based on summary type
            if summary_type == "technical":
                prompt = f"Please provide a technical analysis of the following content. Focus on technical details, implementation considerations, and potential challenges.\n\nContent:\n{content}\n\n{tags_text}"
            elif summary_type == "conceptual":
                prompt = f"Please provide a conceptual explanation of the following content. Focus on the key concepts, their relationships, and their significance.\n\nContent:\n{content}\n\n{tags_text}"
            else:  # general
                prompt = f"Please provide a comprehensive summary of the following content. Include key points, insights, and implications.\n\nContent:\n{content}\n\n{tags_text}"

            # Call OpenAI API (using the latest client version)
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert analyst providing insightful summaries and explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            # Extract summary text
            summary_text = response.choices[0].message.content.strip()

            # Create summary data
            summary = {
                "memory_id": memory.get("memory_id"),
                "summary_type": summary_type,
                "summary_text": summary_text,
                "model": self.model,
                "timestamp": datetime.now().isoformat(),
            }

            logger.info(f"Generated {summary_type} summary for memory {memory.get('memory_id')}")
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return self._generate_mock_summary(memory, summary_type)

    def _generate_mock_summary(
        self,
        memory: Dict[str, Any],
        summary_type: str
    ) -> Dict[str, Any]:
        """
        Generate a mock summary when API is not available.

        Args:
            memory: The memory data
            summary_type: Type of summary to generate

        Returns:
            Mock summary data
        """
        logger.warning(f"Generating mock {summary_type} summary for memory {memory.get('memory_id')}")

        content = memory.get("content", "")

        if summary_type == "technical":
            summary_text = f"Technical Analysis (Mock): This content discusses technical aspects of {content[:50]}..."
        elif summary_type == "conceptual":
            summary_text = f"Conceptual Explanation (Mock): The key concepts in this content are related to {content[:50]}..."
        else:  # general
            summary_text = f"General Summary (Mock): This content is about {content[:50]}..."

        return {
            "memory_id": memory.get("memory_id"),
            "summary_type": summary_type,
            "summary_text": summary_text,
            "model": "mock",
            "timestamp": datetime.now().isoformat(),
        }

    def generate_multiple_summaries(
        self,
        memory: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Generate multiple types of summaries for a memory.

        Args:
            memory: The memory data

        Returns:
            Dictionary of summary types and their data
        """
        summary_types = ["general", "technical", "conceptual"]
        summaries = {}

        for summary_type in summary_types:
            summary = self.generate_summary(memory, summary_type)
            if summary:
                summaries[summary_type] = summary

        logger.info(f"Generated {len(summaries)} summaries for memory {memory.get('memory_id')}")
        return summaries

    def analyze_content(
        self,
        content: str,
        context: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze content without an existing memory.

        Args:
            content: The content to analyze
            context: Additional context for the analysis

        Returns:
            Analysis data or None if analysis failed
        """
        if not self.api_key:
            logger.warning("Cannot analyze content: No OpenAI API key provided")
            return None

        try:
            # Create prompt
            prompt = f"Please analyze the following content and provide insights, key points, and implications.\n\nContent:\n{content}"

            if context:
                prompt += f"\n\nContext:\n{context}"

            # Call OpenAI API (using the latest client version)
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert analyst providing insightful analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            # Extract analysis text
            analysis_text = response.choices[0].message.content.strip()

            # Create analysis data
            analysis = {
                "content": content[:100] + "..." if len(content) > 100 else content,
                "analysis_text": analysis_text,
                "model": self.model,
                "timestamp": datetime.now().isoformat(),
            }

            logger.info("Generated content analysis")
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            return None

    def suggest_tags(
        self,
        content: str
    ) -> List[Dict[str, Any]]:
        """
        Suggest tags for content.

        Args:
            content: The content to suggest tags for

        Returns:
            List of suggested tags
        """
        if not self.api_key:
            logger.warning("Cannot suggest tags: No OpenAI API key provided")
            return []

        try:
            # Create prompt
            prompt = f"""Please suggest tags for the following content.
            Return the tags in JSON format with the following structure:
            [
                {{"type": "category", "value": "tag_value", "score": 0.95}},
                {{"type": "concept", "value": "tag_value", "score": 0.8}},
                ...
            ]

            Content:
            {content}

            JSON Tags:"""

            # Call OpenAI API (using the latest client version)
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at categorizing and tagging content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent output
                max_tokens=self.max_tokens
            )

            # Extract tags text
            tags_text = response.choices[0].message.content.strip()

            # Parse JSON
            try:
                # Find JSON array in the response
                start_idx = tags_text.find("[")
                end_idx = tags_text.rfind("]") + 1

                if start_idx >= 0 and end_idx > start_idx:
                    json_str = tags_text[start_idx:end_idx]
                    tags = json.loads(json_str)
                else:
                    # Fallback if JSON array not found
                    tags = []
            except json.JSONDecodeError:
                logger.warning("Failed to parse tags JSON, using empty list")
                tags = []

            logger.info(f"Generated {len(tags)} suggested tags")
            return tags
        except Exception as e:
            logger.error(f"Error suggesting tags: {str(e)}")
            return []

# FUTURE DEVELOPMENT NOTE:
# In the future, this module will be replaced with an agent-based implementation
# using Google's Agent-to-Agent (A2A) protocol. The agent will be responsible for:
# 1. Generating summaries, explanations, and commentaries
# 2. Analyzing content and suggesting tags
# 3. Communicating with other agents in the system
#
# The agent will be part of a team of specialized AI agents, each with different
# capabilities and responsibilities. This will enable more sophisticated and
# contextual memory processing.
