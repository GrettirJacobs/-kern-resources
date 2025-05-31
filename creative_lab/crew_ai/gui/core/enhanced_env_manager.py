"""
Enhanced Environment Manager

This module provides enhanced environment variable management for the CrewAI GUI.
It handles loading, saving, and retrieving environment variables, with a focus on API keys.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv, set_key

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
DEFAULT_MODELS = {
    'openai': 'gpt-4o',
    'anthropic': 'claude-3-opus-20240229',
    'groq': 'llama-4-70b-instruct',
    'google': 'gemini-1.5-pro'
}

class EnhancedEnvManager:
    """Enhanced environment variable manager."""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize the enhanced environment manager.

        Args:
            env_file: Path to the .env file. If None, will look for .env in the current directory.
        """
        self.env_file = env_file
        if self.env_file is None:
            # Look for .env in the crew_ai directory
            current_dir = Path(__file__).parent
            crew_ai_dir = current_dir.parent
            self.env_file = str(crew_ai_dir / '.env')

        # Load environment variables
        self._load_env()

    def _load_env(self) -> None:
        """Load environment variables from the .env file."""
        try:
            # Check if the .env file exists
            if not os.path.exists(self.env_file):
                logger.warning(f".env file not found at {self.env_file}")
                return

            # Load environment variables
            load_dotenv(self.env_file)
            logger.info(f"Loaded environment variables from {self.env_file}")
        except Exception as e:
            logger.error(f"Failed to load environment variables: {e}")

    def get_api_key(self, provider: str) -> Optional[str]:
        """Get the API key for a provider.

        Args:
            provider: The provider to get the API key for.

        Returns:
            The API key, or None if not found.
        """
        # Map provider to environment variable name
        env_var_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'groq': 'GROQ_API_KEY',
            'google': 'GOOGLE_API_KEY'
        }

        # Get the environment variable name
        env_var = env_var_map.get(provider.lower())
        if not env_var:
            logger.warning(f"Unknown provider: {provider}")
            return None

        # Get the API key from environment variables
        api_key = os.environ.get(env_var)

        # If API key is not found or empty, log a warning
        if not api_key:
            logger.warning(f"API key not found for provider: {provider}")
            return None

        # Log a masked version of the API key for debugging
        if len(api_key) > 8:
            masked_key = api_key[:4] + "..." + api_key[-4:]
            logger.debug(f"Using {provider} API key: {masked_key}")

        return api_key

    def set_api_key(self, provider: str, api_key: str) -> bool:
        """Set the API key for a provider.

        Args:
            provider: The provider to set the API key for.
            api_key: The API key to set.

        Returns:
            True if successful, False otherwise.
        """
        # Map provider to environment variable name
        env_var_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'groq': 'GROQ_API_KEY',
            'google': 'GOOGLE_API_KEY'
        }

        # Get the environment variable name
        env_var = env_var_map.get(provider.lower())
        if not env_var:
            logger.warning(f"Unknown provider: {provider}")
            return False

        # Validate the API key (basic validation)
        if not api_key or len(api_key) < 8:
            logger.warning(f"Invalid API key for provider {provider}: Key is too short or empty")
            return False

        try:
            # Set the environment variable
            os.environ[env_var] = api_key

            # Update the .env file
            set_key(self.env_file, env_var, api_key)

            # Log a masked version of the API key for debugging
            masked_key = api_key[:4] + "..." + api_key[-4:]
            logger.info(f"Set API key for provider {provider}: {masked_key}")
            return True
        except Exception as e:
            logger.error(f"Failed to set API key for provider {provider}: {e}")
            return False

    def get_model(self, provider: str) -> str:
        """Get the default model for a provider.

        Args:
            provider: The provider to get the model for.

        Returns:
            The default model for the provider.
        """
        # Map provider to environment variable name
        env_var_map = {
            'openai': 'OPENAI_MODEL',
            'anthropic': 'ANTHROPIC_MODEL',
            'groq': 'GROQ_MODEL',
            'google': 'GOOGLE_MODEL'
        }

        # Also check these alternative environment variables
        alt_env_var_map = {
            'openai': 'GPT_MODEL',
            'anthropic': 'RESEARCHER_MODEL',
            'groq': 'GROQ_MODEL',
            'google': 'GEMINI_MODEL'
        }

        # Get the environment variable name
        env_var = env_var_map.get(provider.lower())
        alt_env_var = alt_env_var_map.get(provider.lower())

        if not env_var:
            logger.warning(f"Unknown provider: {provider}")
            return DEFAULT_MODELS.get(provider.lower(), '')

        # Try to get the model from the primary environment variable
        model = os.environ.get(env_var)

        # If not found, try the alternative environment variable
        if not model and alt_env_var:
            model = os.environ.get(alt_env_var)

        # If still not found, use the default model
        if not model:
            model = DEFAULT_MODELS.get(provider.lower(), '')
            logger.info(f"Using default model for {provider}: {model}")

        return model

    def set_model(self, provider: str, model: str) -> bool:
        """Set the default model for a provider.

        Args:
            provider: The provider to set the model for.
            model: The model to set.

        Returns:
            True if successful, False otherwise.
        """
        # Map provider to environment variable name
        env_var_map = {
            'openai': 'OPENAI_MODEL',
            'anthropic': 'ANTHROPIC_MODEL',
            'groq': 'GROQ_MODEL',
            'google': 'GOOGLE_MODEL'
        }

        # Get the environment variable name
        env_var = env_var_map.get(provider.lower())
        if not env_var:
            logger.warning(f"Unknown provider: {provider}")
            return False

        try:
            # Set the environment variable
            os.environ[env_var] = model

            # Update the .env file
            set_key(self.env_file, env_var, model)

            logger.info(f"Set model for provider: {provider}")
            return True
        except Exception as e:
            logger.error(f"Failed to set model for provider {provider}: {e}")
            return False

    def get_all_api_keys(self) -> Dict[str, str]:
        """Get all API keys.

        Returns:
            A dictionary mapping provider names to API keys.
        """
        return {
            'openai': self.get_api_key('openai') or '',
            'anthropic': self.get_api_key('anthropic') or '',
            'groq': self.get_api_key('groq') or '',
            'google': self.get_api_key('google') or ''
        }

    def get_all_models(self) -> Dict[str, str]:
        """Get all default models.

        Returns:
            A dictionary mapping provider names to default models.
        """
        return {
            'openai': self.get_model('openai'),
            'anthropic': self.get_model('anthropic'),
            'groq': self.get_model('groq'),
            'google': self.get_model('google')
        }

# Create a singleton instance
env_manager = EnhancedEnvManager()

def get_env_manager() -> EnhancedEnvManager:
    """Get the enhanced environment manager instance.

    Returns:
        The enhanced environment manager instance.
    """
    return env_manager
