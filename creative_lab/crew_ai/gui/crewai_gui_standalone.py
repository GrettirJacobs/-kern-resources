#!/usr/bin/env python3
"""
CrewAI GUI Standalone Entry Point

This is the main entry point for the standalone CrewAI GUI executable.
It handles resource bundling, path resolution, and application initialization.
"""

import os
import sys
import logging
import tempfile
import shutil
from pathlib import Path
import webbrowser
import threading
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('crewai_gui.log')
    ]
)
logger = logging.getLogger(__name__)

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        logger.info(f"Running as PyInstaller bundle, base path: {base_path}")
    except AttributeError:
        # Running in development mode
        base_path = Path(__file__).parent
        logger.info(f"Running in development mode, base path: {base_path}")
    
    resource_path = os.path.join(base_path, relative_path)
    logger.info(f"Resource path for '{relative_path}': {resource_path}")
    return resource_path

def setup_environment():
    """Set up the environment for the standalone application"""
    logger.info("Setting up environment for standalone application...")
    
    # Add the current directory to Python path
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent.parent
    
    # Add paths to sys.path
    paths_to_add = [
        str(project_root),
        str(current_dir),
        str(current_dir.parent),
        str(current_dir.parent.parent)
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
            logger.info(f"Added to Python path: {path}")
    
    # Set environment variables
    os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)
    
    # Load .env file if it exists
    env_file = project_root / "creative_lab" / "crew_ai" / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            logger.info(f"Loaded environment variables from {env_file}")
        except ImportError:
            logger.warning("python-dotenv not available, skipping .env file loading")
    else:
        logger.warning(f"No .env file found at {env_file}")

def check_dependencies():
    """Check if all required dependencies are available"""
    logger.info("Checking dependencies...")
    
    required_modules = [
        'flask',
        'flask_socketio',
        'flask_cors',
        'crewai'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✓ {module} available")
        except ImportError:
            missing_modules.append(module)
            logger.error(f"✗ {module} not available")
    
    if missing_modules:
        logger.error(f"Missing required modules: {missing_modules}")
        return False
    
    logger.info("All dependencies available")
    return True

def create_gui_instance():
    """Create and configure the CrewAI GUI instance"""
    logger.info("Creating CrewAI GUI instance...")

    try:
        # Try multiple import paths
        import_attempts = [
            "apps.crewai.crewai_gui",
            "crewai_gui",
            "creative_lab.crew_ai.gui.apps.crewai.crewai_gui"
        ]

        gui = None
        for import_path in import_attempts:
            try:
                logger.info(f"Trying import: {import_path}")
                if import_path == "apps.crewai.crewai_gui":
                    from apps.crewai.crewai_gui import CrewAIGUI
                elif import_path == "crewai_gui":
                    # Add the apps/crewai directory to path
                    apps_crewai_path = get_resource_path('apps/crewai')
                    if apps_crewai_path not in sys.path:
                        sys.path.insert(0, apps_crewai_path)
                    from crewai_gui import CrewAIGUI
                else:
                    from creative_lab.crew_ai.gui.apps.crewai.crewai_gui import CrewAIGUI

                # Create the GUI instance
                gui = CrewAIGUI(
                    host="127.0.0.1",
                    port=5000,
                    debug=False
                )

                logger.info(f"CrewAI GUI instance created successfully using: {import_path}")
                break

            except ImportError as e:
                logger.warning(f"Import failed for {import_path}: {e}")
                continue

        if gui is None:
            logger.error("All import attempts failed")
            return None

        return gui

    except Exception as e:
        logger.error(f"Failed to create CrewAI GUI instance: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

def open_browser_delayed(url, delay=3):
    """Open browser after a delay"""
    def open_browser():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            logger.info(f"Opened browser to {url}")
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
    
    thread = threading.Thread(target=open_browser)
    thread.daemon = True
    thread.start()

def main():
    """Main entry point for the standalone application"""
    logger.info("=" * 60)
    logger.info("CrewAI GUI Standalone Application Starting...")
    logger.info("=" * 60)
    
    try:
        # Setup environment
        setup_environment()
        
        # Check dependencies
        if not check_dependencies():
            logger.error("Dependency check failed. Cannot start application.")
            input("Press Enter to exit...")
            sys.exit(1)
        
        # Create GUI instance
        gui = create_gui_instance()
        if not gui:
            logger.error("Failed to create GUI instance. Cannot start application.")
            input("Press Enter to exit...")
            sys.exit(1)
        
        # Start the application
        logger.info("Starting CrewAI GUI server...")
        logger.info("Server will be available at: http://127.0.0.1:5000")
        logger.info("Opening browser automatically...")
        
        # Open browser after a delay
        open_browser_delayed("http://127.0.0.1:5000", delay=3)
        
        # Run the GUI
        gui.run(open_browser=False)
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()
