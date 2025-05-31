"""
CrewAI API

This module provides a RESTful API for calling CrewAI programmatically.
It allows users to create agents, tasks, and crews, and to execute them.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import the crew_ai module
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

# Load environment variables from .env file
env_path = current_dir.parent / ".env"
load_dotenv(dotenv_path=env_path)
logger.info(f"Loaded environment variables from {env_path}")

# Import Flask and related modules
try:
    from flask import Flask, request, jsonify, Blueprint
    from flask_cors import CORS
except ImportError:
    logger.error("Flask or related modules not installed. Please install them with:")
    logger.error("pip install flask flask-cors")
    sys.exit(1)

# Try to import the tool system
try:
    from creative_lab.crew_ai.tools.gui_integration import (
        get_tools_for_gui,
        get_tool_categories,
        execute_tool_for_gui,
        configure_tool_for_gui,
        get_tool_status
    )
    TOOLS_AVAILABLE = True
except ImportError:
    logger.warning("Tool system not available. Please install it with 'pip install -e .'")
    TOOLS_AVAILABLE = False

# Try to import CrewAI
try:
    from crewai import Agent, Task, Crew, Process
    CREWAI_AVAILABLE = True
except ImportError:
    logger.warning("CrewAI not available. Please install it with 'pip install crewai'.")
    CREWAI_AVAILABLE = False

# Try to import the CrewAI integration
try:
    from creative_lab.crew_ai.gui.crewai_integration import get_integration
    integration = get_integration()
    INTEGRATION_AVAILABLE = True
except ImportError:
    logger.warning("CrewAI integration not available.")
    integration = None
    INTEGRATION_AVAILABLE = False

# Try to import the enhanced environment manager
try:
    from creative_lab.crew_ai.gui.enhanced_env_manager import get_env_manager
    enhanced_env_manager = get_env_manager()
    ENV_MANAGER_AVAILABLE = True
except ImportError:
    logger.warning("Enhanced environment manager not available.")
    enhanced_env_manager = None
    ENV_MANAGER_AVAILABLE = False

class CrewAIAPI:
    """
    RESTful API for CrewAI.

    This class provides a RESTful API for interacting with CrewAI.
    It allows users to create agents, tasks, and crews, and to execute them.
    """

    def __init__(self):
        """Initialize the CrewAI API."""
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

        # Create the blueprint
        self.bp = Blueprint('crewai_api', __name__, url_prefix='/api')

        # Set up routes
        self._setup_routes()

    def _setup_routes(self):
        """Set up the API routes."""

        @self.bp.route('/status')
        def status():
            """Return the status of the CrewAI integration."""
            logger.info("API request: /status")
            status_info = {
                'crewai_available': CREWAI_AVAILABLE,
                'integration_available': INTEGRATION_AVAILABLE,
                'env_manager_available': ENV_MANAGER_AVAILABLE,
                'tools_available': TOOLS_AVAILABLE
            }

            # Add tool status if available
            if TOOLS_AVAILABLE:
                try:
                    tool_status = get_tool_status()
                    status_info['tools'] = tool_status
                except Exception as e:
                    logger.error(f"Error getting tool status: {e}")
                    status_info['tools_error'] = str(e)

            return jsonify(status_info)

        @self.bp.route('/models')
        def models():
            """Return the available models."""
            logger.info("API request: /models")
            if ENV_MANAGER_AVAILABLE:
                logger.info("Using enhanced environment manager to get models")
                return jsonify({
                    'openai': enhanced_env_manager.get_model('openai'),
                    'anthropic': enhanced_env_manager.get_model('anthropic'),
                    'groq': enhanced_env_manager.get_model('groq'),
                    'google': enhanced_env_manager.get_model('google')
                })
            else:
                logger.info("Using default models")
                return jsonify({
                    'openai': 'gpt-3.5-turbo',
                    'anthropic': 'claude-3-sonnet',
                    'groq': 'meta-llama/llama-4-maverick-17b-128e-instruct',
                    'google': 'gemini-1.5-pro'
                })

        @self.bp.route('/agents', methods=['GET', 'POST'])
        def agents_api():
            """Get all agents or create a new agent."""
            logger.info(f"API request: /agents ({request.method})")
            if request.method == 'GET':
                return jsonify(self.agents)
            elif request.method == 'POST':
                logger.info("Creating a new agent")
                try:
                    data = request.json
                    logger.info(f"Request data: {data}")
                    agent_id = data.get('id', f"agent_{len(self.agents) + 1}")
                    logger.info(f"Agent ID: {agent_id}")

                    # Create the agent
                    if INTEGRATION_AVAILABLE and self.integration:
                        logger.info("Integration available, creating agent")
                        try:
                            agent = self.integration.create_agent(
                                role=data.get('role', 'Agent'),
                                goal=data.get('goal', 'Complete tasks'),
                                backstory=data.get('backstory', 'You are an AI agent.'),
                                verbose=data.get('verbose', True),
                                allow_delegation=data.get('allow_delegation', False),
                                llm_config=data.get('llm_config', None)
                            )
                            logger.info("Agent created successfully")

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
                            logger.info(f"Agent stored with ID: {agent_id}")

                            return jsonify({'id': agent_id, 'status': 'created'})
                        except Exception as e:
                            logger.error(f"Failed to create agent: {e}")
                            return jsonify({'error': str(e)}), 500
                    else:
                        logger.error("CrewAI integration not available")
                        return jsonify({'error': 'CrewAI integration not available'}), 500
                except Exception as e:
                    logger.error(f"Error processing agent creation request: {e}")
                    return jsonify({'error': f"Error processing request: {str(e)}"}), 400

        @self.bp.route('/agents/<agent_id>', methods=['DELETE'])
        def delete_agent(agent_id):
            """Delete an agent."""
            if agent_id in self.agents:
                del self.agents[agent_id]
                return jsonify({'status': 'deleted'})
            else:
                return jsonify({'error': f"Agent {agent_id} not found"}), 404

        @self.bp.route('/tasks', methods=['GET', 'POST'])
        def tasks_api():
            """Get all tasks or create a new task."""
            if request.method == 'GET':
                return jsonify({k: {kk: vv for kk, vv in v.items() if kk != 'task'}
                               for k, v in self.tasks.items()})
            elif request.method == 'POST':
                data = request.json
                task_id = data.get('id', f"task_{len(self.tasks) + 1}")
                agent_id = data.get('agent_id')

                if agent_id not in self.agents:
                    return jsonify({'error': f"Agent {agent_id} not found"}), 404

                # Create the task
                if INTEGRATION_AVAILABLE and self.integration:
                    try:
                        task = self.integration.create_task(
                            description=data.get('description', 'Complete this task'),
                            expected_output=data.get('expected_output', 'Task output'),
                            agent=self.agents[agent_id]['agent'],
                            context=data.get('context', [])
                        )

                        # Store the task
                        self.tasks[task_id] = {
                            'id': task_id,
                            'description': data.get('description', 'Complete this task'),
                            'expected_output': data.get('expected_output', 'Task output'),
                            'agent_id': agent_id,
                            'context': data.get('context', []),
                            'task': task
                        }

                        return jsonify({'id': task_id, 'status': 'created'})
                    except Exception as e:
                        logger.error(f"Failed to create task: {e}")
                        return jsonify({'error': str(e)}), 500
                else:
                    return jsonify({'error': 'CrewAI integration not available'}), 500

        @self.bp.route('/tasks/<task_id>', methods=['DELETE'])
        def delete_task(task_id):
            """Delete a task."""
            if task_id in self.tasks:
                del self.tasks[task_id]
                return jsonify({'status': 'deleted'})
            else:
                return jsonify({'error': f"Task {task_id} not found"}), 404

        @self.bp.route('/crews', methods=['GET', 'POST'])
        def crews_api():
            """Get all crews or create a new crew."""
            if request.method == 'GET':
                return jsonify({k: {kk: vv for kk, vv in v.items() if kk != 'crew'}
                               for k, v in self.crews.items()})
            elif request.method == 'POST':
                data = request.json
                crew_id = data.get('id', f"crew_{len(self.crews) + 1}")
                agent_ids = data.get('agent_ids', [])
                task_ids = data.get('task_ids', [])

                # Check if all agents and tasks exist
                for agent_id in agent_ids:
                    if agent_id not in self.agents:
                        return jsonify({'error': f"Agent {agent_id} not found"}), 404

                for task_id in task_ids:
                    if task_id not in self.tasks:
                        return jsonify({'error': f"Task {task_id} not found"}), 404

                # Create the crew
                if INTEGRATION_AVAILABLE and self.integration:
                    try:
                        agents = [self.agents[agent_id]['agent'] for agent_id in agent_ids]
                        tasks = [self.tasks[task_id]['task'] for task_id in task_ids]

                        crew = self.integration.create_crew(
                            agents=agents,
                            tasks=tasks,
                            process=data.get('process', 'sequential'),
                            verbose=data.get('verbose', True),
                            name=data.get('name', f"Crew {crew_id}")
                        )

                        # Store the crew
                        self.crews[crew_id] = {
                            'id': crew_id,
                            'name': data.get('name', f"Crew {crew_id}"),
                            'agent_ids': agent_ids,
                            'task_ids': task_ids,
                            'process': data.get('process', 'sequential'),
                            'verbose': data.get('verbose', True),
                            'crew': crew
                        }

                        return jsonify({'id': crew_id, 'status': 'created'})
                    except Exception as e:
                        logger.error(f"Failed to create crew: {e}")
                        return jsonify({'error': str(e)}), 500
                else:
                    return jsonify({'error': 'CrewAI integration not available'}), 500

        @self.bp.route('/crews/<crew_id>', methods=['DELETE'])
        def delete_crew(crew_id):
            """Delete a crew."""
            if crew_id in self.crews:
                del self.crews[crew_id]
                return jsonify({'status': 'deleted'})
            else:
                return jsonify({'error': f"Crew {crew_id} not found"}), 404

        @self.bp.route('/crews/<crew_id>/run', methods=['POST'])
        def run_crew(crew_id):
            """Run a crew."""
            if crew_id not in self.crews:
                return jsonify({'error': f"Crew {crew_id} not found"}), 404

            # Run the crew
            try:
                crew = self.crews[crew_id]['crew']
                result = self.integration.run_crew(crew)

                # Store the result
                self.results[crew_id] = result

                return jsonify({'status': 'completed', 'result': result})
            except ValueError as ve:
                # Handle specific errors like API key issues
                error_str = str(ve).lower()
                if 'api key' in error_str:
                    logger.error(f"API key error when running crew: {ve}")
                    return jsonify({
                        'error': str(ve),
                        'error_type': 'api_key_error',
                        'message': 'Please check your API keys in the settings.'
                    }), 401  # Unauthorized status code for auth issues
                else:
                    logger.error(f"Value error when running crew: {ve}")
                    return jsonify({
                        'error': str(ve),
                        'error_type': 'value_error'
                    }), 400  # Bad request for value errors
            except Exception as e:
                logger.error(f"Failed to run crew: {e}")
                return jsonify({
                    'error': str(e),
                    'error_type': 'unknown_error'
                }), 500

        @self.bp.route('/results/<crew_id>', methods=['GET'])
        def get_result(crew_id):
            """Get the result of a crew run."""
            if crew_id not in self.results:
                return jsonify({'error': f"No results for crew {crew_id}"}), 404

            return jsonify({'result': self.results[crew_id]})

        @self.bp.route('/configs', methods=['GET', 'POST'])
        def configs_api():
            """Get or save configurations."""
            if request.method == 'GET':
                # Load configurations from file
                config_file = os.path.join(current_dir, 'configs', 'crews.json')
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        return jsonify(json.load(f))
                else:
                    return jsonify({})
            elif request.method == 'POST':
                # Save configurations to file
                data = request.json

                # Create configs directory if it doesn't exist
                os.makedirs(os.path.join(current_dir, 'configs'), exist_ok=True)

                # Save the configurations
                config_file = os.path.join(current_dir, 'configs', 'crews.json')
                with open(config_file, 'w') as f:
                    json.dump(data, f, indent=2)

                return jsonify({'status': 'saved'})

        @self.bp.route('/configs/<config_id>', methods=['GET'])
        def get_config(config_id):
            """Get a configuration."""
            config_file = os.path.join(current_dir, 'configs', 'crews.json')
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    configs = json.load(f)
                    if config_id in configs:
                        return jsonify(configs[config_id])
                    else:
                        return jsonify({'error': f"Configuration {config_id} not found"}), 404
            else:
                return jsonify({'error': "No configurations found"}), 404

        @self.bp.route('/settings', methods=['GET', 'POST'])
        def settings_api():
            """Get or save settings."""
            if request.method == 'GET':
                # Load settings from file
                settings_file = os.path.join(current_dir, 'configs', 'settings.json')
                if os.path.exists(settings_file):
                    with open(settings_file, 'r') as f:
                        return jsonify(json.load(f))
                else:
                    return jsonify({})
            elif request.method == 'POST':
                # Save settings to file
                data = request.json

                # Create configs directory if it doesn't exist
                os.makedirs(os.path.join(current_dir, 'configs'), exist_ok=True)

                # Save the settings
                settings_file = os.path.join(current_dir, 'configs', 'settings.json')
                with open(settings_file, 'w') as f:
                    json.dump(data, f, indent=2)

                # Update API keys if provided
                if ENV_MANAGER_AVAILABLE and enhanced_env_manager:
                    api_keys = data.get('api_keys', {})
                    for provider, api_key in api_keys.items():
                        if api_key and len(api_key) > 8:  # Basic validation
                            enhanced_env_manager.set_api_key(provider, api_key)

                # Update default models if provided
                if ENV_MANAGER_AVAILABLE and enhanced_env_manager:
                    models = data.get('models', {})
                    for provider, model in models.items():
                        if model:
                            enhanced_env_manager.set_model(provider, model)

                return jsonify({'status': 'saved'})

        @self.bp.route('/api-keys', methods=['GET', 'POST'])
        def api_keys_api():
            """Get or update API keys."""
            if request.method == 'GET':
                # Get API keys from environment manager
                if ENV_MANAGER_AVAILABLE and enhanced_env_manager:
                    api_keys = {
                        'openai': enhanced_env_manager.get_api_key('openai'),
                        'anthropic': enhanced_env_manager.get_api_key('anthropic'),
                        'groq': enhanced_env_manager.get_api_key('groq'),
                        'google': enhanced_env_manager.get_api_key('google')
                    }
                    # Mask API keys for security
                    masked_keys = {}
                    for provider, key in api_keys.items():
                        if key and len(key) > 8:
                            masked_keys[provider] = key[:4] + '...' + key[-4:]
                        else:
                            masked_keys[provider] = None
                    return jsonify({
                        'api_keys': masked_keys,
                        'status': 'available'
                    })
                else:
                    return jsonify({
                        'api_keys': {},
                        'status': 'unavailable',
                        'message': 'Environment manager not available'
                    })
            elif request.method == 'POST':
                # Update API keys
                data = request.json
                api_keys = data.get('api_keys', {})

                if ENV_MANAGER_AVAILABLE and enhanced_env_manager:
                    results = {}
                    for provider, api_key in api_keys.items():
                        if api_key and len(api_key) > 8:  # Basic validation
                            success = enhanced_env_manager.set_api_key(provider, api_key)
                            results[provider] = 'updated' if success else 'failed'
                        else:
                            results[provider] = 'invalid'

                    return jsonify({
                        'status': 'updated',
                        'results': results
                    })
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Environment manager not available'
                    }), 500

        # Tool endpoints

        @self.bp.route('/tools', methods=['GET'])
        def tools_api():
            """Get all available tools."""
            logger.info("API request: /tools")
            if TOOLS_AVAILABLE:
                try:
                    tools = get_tools_for_gui()
                    return jsonify({
                        'tools': tools,
                        'status': 'available'
                    })
                except Exception as e:
                    logger.error(f"Error getting tools: {e}")
                    return jsonify({
                        'error': str(e),
                        'status': 'error'
                    }), 500
            else:
                return jsonify({
                    'tools': [],
                    'status': 'unavailable',
                    'message': 'Tool system not available'
                })

        @self.bp.route('/tools/categories', methods=['GET'])
        def tool_categories_api():
            """Get all tool categories."""
            logger.info("API request: /tools/categories")
            if TOOLS_AVAILABLE:
                try:
                    categories = get_tool_categories()
                    return jsonify({
                        'categories': categories,
                        'status': 'available'
                    })
                except Exception as e:
                    logger.error(f"Error getting tool categories: {e}")
                    return jsonify({
                        'error': str(e),
                        'status': 'error'
                    }), 500
            else:
                return jsonify({
                    'categories': [],
                    'status': 'unavailable',
                    'message': 'Tool system not available'
                })

        @self.bp.route('/tools/<tool_name>/execute', methods=['POST'])
        def execute_tool_api(tool_name):
            """Execute a tool."""
            logger.info(f"API request: /tools/{tool_name}/execute")
            if TOOLS_AVAILABLE:
                try:
                    data = request.json
                    parameters = data.get('parameters', {})

                    result = execute_tool_for_gui(tool_name, parameters)
                    return jsonify(result)
                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {e}")
                    return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 500
            else:
                return jsonify({
                    'success': False,
                    'error': 'Tool system not available'
                }), 500

        @self.bp.route('/tools/<tool_name>/configure', methods=['POST'])
        def configure_tool_api(tool_name):
            """Configure a tool."""
            logger.info(f"API request: /tools/{tool_name}/configure")
            if TOOLS_AVAILABLE:
                try:
                    data = request.json
                    config = data.get('config', {})

                    result = configure_tool_for_gui(tool_name, config)
                    return jsonify(result)
                except Exception as e:
                    logger.error(f"Error configuring tool {tool_name}: {e}")
                    return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 500
            else:
                return jsonify({
                    'success': False,
                    'error': 'Tool system not available'
                }), 500

        @self.bp.route('/agents/<agent_id>/tools', methods=['GET', 'POST'])
        def agent_tools_api(agent_id):
            """Get or assign tools to an agent."""
            logger.info(f"API request: /agents/{agent_id}/tools ({request.method})")

            # Check if the agent exists
            if agent_id not in self.agents:
                return jsonify({'error': f"Agent {agent_id} not found"}), 404

            if request.method == 'GET':
                # Get the tools assigned to the agent
                agent_data = self.agents[agent_id]
                tools = agent_data.get('tools', [])

                return jsonify({
                    'agent_id': agent_id,
                    'tools': tools
                })
            elif request.method == 'POST':
                # Assign tools to the agent
                if not TOOLS_AVAILABLE:
                    return jsonify({
                        'success': False,
                        'error': 'Tool system not available'
                    }), 500

                try:
                    data = request.json
                    tool_names = data.get('tool_names', [])

                    # Update the agent data
                    self.agents[agent_id]['tools'] = tool_names

                    # If we have integration available, update the agent
                    if INTEGRATION_AVAILABLE and self.integration and CREWAI_AVAILABLE:
                        from creative_lab.crew_ai.tools.crewai_integration import assign_tools_to_agent

                        # Get the agent
                        agent = self.agents[agent_id]['agent']

                        # Assign tools to the agent
                        agent = assign_tools_to_agent(agent, tool_names)

                        # Update the agent in the store
                        self.agents[agent_id]['agent'] = agent

                    return jsonify({
                        'success': True,
                        'agent_id': agent_id,
                        'tools': tool_names
                    })
                except Exception as e:
                    logger.error(f"Error assigning tools to agent {agent_id}: {e}")
                    return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 500

def create_api():
    """Create the CrewAI API."""
    return CrewAIAPI()

def register_api(app):
    """Register the CrewAI API with a Flask app."""
    api = create_api()
    app.register_blueprint(api.bp)
    return api

def create_app():
    """Create a Flask app with the CrewAI API."""
    app = Flask(__name__)
    CORS(app)
    register_api(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
