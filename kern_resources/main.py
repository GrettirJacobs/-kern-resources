"""
Kern Resources - Main Entry Point

This module provides the main entry point for the Kern Resources application.
"""

import argparse
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("kern_resources.log")
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Kern Resources")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--env", help="Path to environment file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    # Set logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Import here to avoid circular imports
    from kern_resources.core.utils.config import config
    from kern_resources.core.utils.env_manager import env_manager
    from kern_resources.core.utils.docker_manager import docker_manager
    
    # Load environment variables
    if args.env:
        env_manager.env_files = [args.env]
    env_manager.load()
    
    # Load configuration
    if args.config:
        config.config_path = args.config
        config.reload()
    
    # Ensure Docker and Qdrant are running
    if not docker_manager.is_docker_running():
        logger.info("Docker is not running, attempting to start...")
        if not docker_manager.start_docker():
            logger.error("Failed to start Docker, some features may not work correctly")
    
    if not docker_manager.ensure_qdrant_running():
        logger.error("Failed to ensure Qdrant is running, vector storage features may not work correctly")
    
    # TODO: Initialize and run the application
    logger.info("Kern Resources initialized")
    logger.info(f"Using configuration from: {config.config_path}")
    logger.info(f"Environment files loaded: {', '.join(env_manager.loaded_files) or 'None'}")

if __name__ == "__main__":
    main()
