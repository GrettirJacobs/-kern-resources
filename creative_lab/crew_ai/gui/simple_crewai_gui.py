#!/usr/bin/env python3
"""
Simple CrewAI GUI Standalone Entry Point

A simplified version that focuses on core functionality without complex imports.
"""

import os
import sys
import logging
import webbrowser
import threading
import time
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('simple_crewai_gui.log')
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

def create_simple_flask_app():
    """Create a simple Flask app without complex dependencies"""
    logger.info("Creating simple Flask app...")
    
    try:
        from flask import Flask, render_template, jsonify
        from flask_cors import CORS
        
        # Create Flask app with template and static paths
        template_folder = get_resource_path('templates')
        static_folder = get_resource_path('static')
        
        app = Flask(__name__, 
                   template_folder=template_folder,
                   static_folder=static_folder)
        
        # Enable CORS
        CORS(app)
        
        @app.route('/')
        def index():
            """Render the main page."""
            logger.info("Serving index page")
            try:
                return render_template('index.html')
            except Exception as e:
                logger.error(f"Error rendering index.html: {e}")
                return f"""
                <html>
                <head><title>CrewAI GUI</title></head>
                <body>
                    <h1>CrewAI GUI</h1>
                    <p>Welcome to the CrewAI GUI!</p>
                    <p>This is a simplified version running as a standalone executable.</p>
                    <p>Status: Server is running successfully!</p>
                    <p>Template error: {str(e)}</p>
                </body>
                </html>
                """
        
        @app.route('/test')
        def test():
            """Test route to verify the server is working."""
            logger.info("Test endpoint accessed")
            return jsonify({
                "status": "success",
                "message": "CrewAI GUI is working!",
                "version": "standalone"
            })
        
        @app.route('/health')
        def health():
            """Health check endpoint."""
            return jsonify({
                "status": "healthy",
                "timestamp": time.time()
            })
        
        logger.info("Simple Flask app created successfully")
        return app
        
    except ImportError as e:
        logger.error(f"Failed to import Flask: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to create Flask app: {e}")
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
    """Main entry point for the simple standalone application"""
    logger.info("=" * 60)
    logger.info("Simple CrewAI GUI Standalone Application Starting...")
    logger.info("=" * 60)
    
    try:
        # Setup environment
        setup_environment()
        
        # Create simple Flask app
        app = create_simple_flask_app()
        if not app:
            logger.error("Failed to create Flask app. Cannot start application.")
            input("Press Enter to exit...")
            sys.exit(1)
        
        # Start the application
        logger.info("Starting Simple CrewAI GUI server...")
        logger.info("Server will be available at: http://127.0.0.1:5000")
        logger.info("Opening browser automatically...")
        
        # Open browser after a delay
        open_browser_delayed("http://127.0.0.1:5000", delay=3)
        
        # Run the Flask app
        app.run(host="127.0.0.1", port=5000, debug=False)
        
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
