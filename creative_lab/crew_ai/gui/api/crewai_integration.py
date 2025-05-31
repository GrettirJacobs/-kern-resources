"""
CrewAI Integration Module

This module provides integration between the CrewAI GUI and the CrewAI library.
It handles the creation of agents, tasks, and crews, and the execution of crews.
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import the crew_ai module
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

try:
    import crewai
    from crewai import Agent, Task, Crew, Process
    from creative_lab.crew_ai.llm_helper import create_llm_for_crewai as create_llm
    CREWAI_AVAILABLE = True
    logger.info("CrewAI is available.")
except ImportError as e:
    logger.warning(f"CrewAI not available. Some functionality will be limited. Error: {e}")
    CREWAI_AVAILABLE = False

class CrewAIIntegration:
    """Integration with CrewAI."""

    def __init__(self):
        """Initialize the CrewAI integration."""
        self.agents = {}
        self.tasks = {}
        self.crews = {}

        if not CREWAI_AVAILABLE:
            logger.warning("CrewAI not available. Integration will be limited.")

    def create_agent(self, role: str, goal: str, backstory: str, verbose: bool = True,
                    allow_delegation: bool = False, llm_config: Optional[Dict[str, Any]] = None) -> Any:
        """Create a CrewAI agent.

        Args:
            role: The role of the agent.
            goal: The goal of the agent.
            backstory: The backstory of the agent.
            verbose: Whether to enable verbose output.
            allow_delegation: Whether to allow delegation to other agents.
            llm_config: Configuration for the LLM.

        Returns:
            The created agent.

        Raises:
            ValueError: If CrewAI is not available or if there's an issue with the API key.
        """
        if not CREWAI_AVAILABLE:
            error_msg = "CrewAI not available. Cannot create agent."
            logger.warning(error_msg)
            raise ValueError(error_msg)

        try:
            # Create the LLM
            llm = None
            if llm_config:
                provider = llm_config.get('provider', 'openai')
                model = llm_config.get('model')
                temperature = llm_config.get('temperature', 0.7)

                try:
                    llm = create_llm(provider=provider, model_name=model, temperature=temperature)
                except Exception as llm_error:
                    # Check if it's an API key issue
                    error_str = str(llm_error).lower()
                    if 'api key' in error_str or 'authentication' in error_str or 'auth' in error_str:
                        error_msg = f"API key error for {provider}: {llm_error}"
                        logger.error(error_msg)
                        raise ValueError(f"API key error for {provider}. Please check your API key in the settings.")
                    else:
                        # Re-raise the original error
                        raise

            # Create the agent
            agent = Agent(
                role=role,
                goal=goal,
                backstory=backstory,
                verbose=verbose,
                allow_delegation=allow_delegation,
                llm=llm
            )

            return agent
        except ValueError:
            # Re-raise ValueError (like API key errors) directly
            raise
        except Exception as e:
            error_msg = f"Failed to create agent: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def create_task(self, description: str, expected_output: str, agent: Any,
                   context: Optional[List[Any]] = None) -> Any:
        """Create a CrewAI task.

        Args:
            description: The description of the task.
            expected_output: The expected output of the task.
            agent: The agent to assign the task to.
            context: Additional context for the task.

        Returns:
            The created task.
        """
        if not CREWAI_AVAILABLE:
            logger.warning("CrewAI not available. Cannot create task.")
            return None

        try:
            # Create the task
            task = Task(
                description=description,
                expected_output=expected_output,
                agent=agent,
                context=context or []
            )

            return task
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            raise

    def create_crew(self, agents: List[Any], tasks: List[Any], process: str = "sequential",
                   verbose: bool = True, name: Optional[str] = None) -> Any:
        """Create a CrewAI crew.

        Args:
            agents: The agents to include in the crew.
            tasks: The tasks to assign to the crew.
            process: The process to use for task execution.
            verbose: Whether to enable verbose output.
            name: The name of the crew.

        Returns:
            The created crew.
        """
        if not CREWAI_AVAILABLE:
            logger.warning("CrewAI not available. Cannot create crew.")
            return None

        try:
            # Determine the process
            crew_process = Process.sequential
            if process.lower() == "hierarchical":
                crew_process = Process.hierarchical

            # Create the crew
            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=crew_process,
                verbose=verbose,
                name=name
            )

            return crew
        except Exception as e:
            logger.error(f"Failed to create crew: {e}")
            raise

    def run_crew(self, crew: Any) -> str:
        """Run a CrewAI crew.

        Args:
            crew: The crew to run.

        Returns:
            The result of the crew execution.

        Raises:
            ValueError: If CrewAI is not available or if there's an issue with the API key.
        """
        if not CREWAI_AVAILABLE:
            error_msg = "CrewAI not available. Cannot run crew."
            logger.warning(error_msg)
            raise ValueError(error_msg)

        try:
            # Run the crew
            result = crew.kickoff()

            return result
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's an API key issue
            if 'api key' in error_str or 'authentication' in error_str or 'auth' in error_str:
                error_msg = f"API key error when running crew: {e}"
                logger.error(error_msg)
                raise ValueError(f"API key error when running crew. Please check your API keys in the settings.")
            else:
                error_msg = f"Failed to run crew: {e}"
                logger.error(error_msg)
                raise ValueError(error_msg)

# Create a singleton instance
integration = CrewAIIntegration()

def get_integration() -> CrewAIIntegration:
    """Get the CrewAI integration instance.

    Returns:
        The CrewAI integration instance.
    """
    return integration
