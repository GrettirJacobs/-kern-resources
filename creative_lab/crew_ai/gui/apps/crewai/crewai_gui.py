"""
CrewAI GUI

This module provides a web-based GUI for interacting with CrewAI.
It allows users to create agents, tasks, and crews, and to execute them.
The GUI can be used standalone or integrated with VS Code.
"""

import os
import sys
import json
import logging
import threading
import webbrowser
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import the crew_ai module
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

# Import Flask and related modules
try:
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from flask_socketio import SocketIO, emit
    from flask_cors import CORS
except ImportError:
    logger.error("Flask or related modules not installed. Please install them with:")
    logger.error("pip install flask flask-socketio flask-cors")
    sys.exit(1)

# Try to import CrewAI
try:
    from crewai import Agent, Task, Crew, Process
    CREWAI_AVAILABLE = True
except ImportError:
    logger.warning("CrewAI not available. Please install it with 'pip install crewai'.")
    CREWAI_AVAILABLE = False

# Try to import the CrewAI integration
try:
    from creative_lab.crew_ai.gui.api.crewai_integration import get_integration
    integration = get_integration()
    INTEGRATION_AVAILABLE = True
except ImportError:
    logger.warning("CrewAI integration not available.")
    integration = None
    INTEGRATION_AVAILABLE = False

# Try to import the enhanced environment manager
try:
    from creative_lab.crew_ai.gui.core.enhanced_env_manager import get_env_manager
    enhanced_env_manager = get_env_manager()
    ENV_MANAGER_AVAILABLE = True
except ImportError:
    logger.warning("Enhanced environment manager not available.")
    enhanced_env_manager = None
    ENV_MANAGER_AVAILABLE = False

class CrewAIGUI:
    """
    Web-based GUI for CrewAI.

    This class provides a web-based GUI for interacting with CrewAI.
    It allows users to create agents, tasks, and crews, and to execute them.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5000, debug: bool = False):
        """
        Initialize the CrewAI GUI.

        Args:
            host: The host to run the server on.
            port: The port to run the server on.
            debug: Whether to run the server in debug mode.
        """
        self.host = host
        self.port = port
        self.debug = debug

        # Create the Flask app with correct paths to templates and static folders
        gui_root = current_dir.parent.parent  # Go up to gui directory
        self.app = Flask(__name__,
                         template_folder=os.path.join(gui_root, 'templates'),
                         static_folder=os.path.join(gui_root, 'static'))

        # Enable CORS
        CORS(self.app)

        # Create the SocketIO instance
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        # Initialize CrewAI integration
        self.integration = None
        if INTEGRATION_AVAILABLE and integration:
            try:
                self.integration = integration
                logger.info("CrewAI integration initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize CrewAI integration: {e}")

        # Store agents, tasks, and crews
        self.agents = {}
        self.tasks = {}
        self.crews = {}
        self.results = {}

        # Import and register the APIs
        from creative_lab.crew_ai.gui.api.crewai_api import register_api
        self.api = register_api(self.app)

        # Register the Excel API
        try:
            from creative_lab.crew_ai.gui.api.excel_api import register_excel_api
            register_excel_api(self.app)
            logger.info("Excel API registered")
        except ImportError as e:
            logger.warning(f"Excel API not available: {e}")

        # Register the Simple Excel Analysis API
        try:
            from creative_lab.crew_ai.gui.api.simple_excel_api import register_simple_excel_api
            register_simple_excel_api(self.app)
            logger.info("Simple Excel Analysis API registered")
        except ImportError as e:
            logger.warning(f"Simple Excel Analysis API not available: {e}")

        # Register the Excel Analysis API (with CrewAI)
        try:
            from creative_lab.crew_ai.gui.api.excel_analysis_api import register_excel_analysis_api
            register_excel_analysis_api(self.app)
            logger.info("Excel Analysis API registered")
        except ImportError as e:
            logger.warning(f"Excel Analysis API not available: {e}")

        # Set up routes
        self._setup_routes()

        # Set up SocketIO events
        self._setup_socketio_events()

    def _setup_routes(self):
        """Set up the Flask routes."""
        logger.info("Setting up Flask routes...")

        @self.app.route('/')
        def index():
            """Render the main page."""
            logger.info("API request: / (index)")
            try:
                return render_template('index.html')
            except Exception as e:
                logger.error(f"Error rendering index.html: {e}")
                return f"<h1>Error</h1><p>{str(e)}</p>"

        @self.app.route('/vscode-extension')
        def vscode_extension():
            """Return the VS Code extension."""
            logger.info("Returning VS Code extension")
            try:
                return send_from_directory(os.path.join(current_dir, 'vscode-extension'), 'crewai-vscode-extension.vsix')
            except Exception as e:
                logger.error(f"Error returning VS Code extension: {e}")
                return f"<h1>Error</h1><p>{str(e)}</p>"

        @self.app.route('/test')
        def test():
            """Test route to verify the server is working."""
            logger.info("API request: /test")
            return "<h1>CrewAI GUI is working!</h1>"

        @self.app.route('/test-upload')
        def test_upload():
            """Test route to verify template rendering."""
            logger.info("API request: /test-upload")
            try:
                return render_template('test_upload.html')
            except Exception as e:
                logger.error(f"Error rendering test_upload.html: {e}")
                return f"<h1>Error</h1><p>{str(e)}</p>"

        @self.app.route('/simple-upload')
        def simple_upload():
            """Render the simple upload page."""
            logger.info("API request: /simple-upload")
            try:
                return render_template('simple_upload.html')
            except Exception as e:
                logger.error(f"Error rendering simple_upload.html: {e}")
                return f"<h1>Error</h1><p>{str(e)}</p>"

        @self.app.route('/basic-upload')
        def basic_upload():
            """Render the basic upload page."""
            logger.info("API request: /basic-upload")
            try:
                return render_template('basic_upload.html')
            except Exception as e:
                logger.error(f"Error rendering basic_upload.html: {e}")
                return f"<h1>Error</h1><p>{str(e)}</p>"

        @self.app.route('/analyze-excel')
        def analyze_excel():
            """Render the analyze Excel page."""
            logger.info("API request: /analyze-excel")
            try:
                return render_template('analyze_excel.html')
            except Exception as e:
                logger.error(f"Error rendering analyze_excel.html: {e}")
                return f"<h1>Error</h1><p>{str(e)}</p>"

        @self.app.route('/simple-analyze-excel')
        def simple_analyze_excel():
            """Render the simple analyze Excel page."""
            logger.info("API request: /simple-analyze-excel")
            try:
                return render_template('simple_analyze_excel.html')
            except Exception as e:
                logger.error(f"Error rendering simple_analyze_excel.html: {e}")
                return f"<h1>Error</h1><p>{str(e)}</p>"

        @self.app.route('/upload')
        def upload():
            """Render the upload page."""
            logger.info("API request: /upload")
            try:
                # Add debug information
                template_folder = self.app.template_folder
                available_templates = os.listdir(template_folder)
                logger.info(f"Template folder: {template_folder}")
                logger.info(f"Available templates: {available_templates}")

                return render_template('upload.html')
            except Exception as e:
                logger.error(f"Error rendering upload page: {e}")
                return f"<h1>Error</h1><p>{str(e)}</p><p>Template folder: {self.app.template_folder}</p><p>Available templates: {os.listdir(self.app.template_folder)}</p>"

    def _setup_socketio_events(self):
        """Set up the SocketIO events."""

        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            logger.info("Client connected")

        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            logger.info("Client disconnected")

        @self.socketio.on('create_agent')
        def handle_create_agent(data):
            """Handle agent creation."""
            agent_id = data.get('id', f"agent_{len(self.agents) + 1}")

            # Create the agent
            if INTEGRATION_AVAILABLE and self.integration:
                try:
                    agent = self.integration.create_agent(
                        role=data.get('role', 'Agent'),
                        goal=data.get('goal', 'Complete tasks'),
                        backstory=data.get('backstory', 'You are an AI agent.'),
                        verbose=data.get('verbose', True),
                        allow_delegation=data.get('allow_delegation', False),
                        llm_config=data.get('llm_config', None)
                    )

                    # Store the agent
                    self.agents[agent_id] = {
                        'id': agent_id,
                        'role': data.get('role', 'Agent'),
                        'goal': data.get('goal', 'Complete tasks'),
                        'backstory': data.get('backstory', 'You are an AI agent.'),
                        'verbose': data.get('verbose', True),
                        'allow_delegation': data.get('allow_delegation', False),
                        'llm_config': data.get('llm_config', None),
                        'agent': agent
                    }

                    emit('agent_created', {'id': agent_id, 'status': 'created'})
                except Exception as e:
                    logger.error(f"Failed to create agent: {e}")
                    emit('agent_error', {'error': str(e)})
            else:
                emit('agent_error', {'error': 'CrewAI integration not available'})

    def run(self, open_browser: bool = False):
        """
        Run the CrewAI GUI.

        Args:
            open_browser: Whether to open the browser automatically. Defaults to False.
        """
        if open_browser:
            # Open the browser
            url = f"http://{self.host}:{self.port}"
            threading.Timer(1.0, lambda: webbrowser.open(url)).start()
            logger.info(f"Opening browser at {url}")

        # Run the server
        self.socketio.run(self.app, host=self.host, port=self.port, debug=self.debug)

def main():
    """Run the CrewAI GUI."""
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='CrewAI GUI')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--open-browser', action='store_true', help='Open the browser automatically')
    args = parser.parse_args()

    # Create and run the GUI
    gui = CrewAIGUI(host=args.host, port=args.port, debug=args.debug)
    gui.run(open_browser=args.open_browser)

if __name__ == '__main__':
    main()
