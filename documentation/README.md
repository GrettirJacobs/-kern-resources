# Kern Resources Documentation

This directory contains documentation for the Kern Resources project, including guides, implementation details, and best practices.

## ChainLit Integration

- [ChainLit Integration Guide](chainlit_integration_guide.md) - Comprehensive guide for integrating ChainLit with the Kern Resources project
- [ChainLit Fixes Implementation](chainlit_fixes_implementation.md) - Details of the fixes implemented to resolve ChainLit integration issues
- [A2A and MCP Integration](a2a_mcp_integration.md) - Guide for integrating Agent-to-Agent (A2A) protocol and Model Context Protocol (MCP) with ChainLit

## Running the Application

To run the ChainLit UI:

```bash
# Run the comprehensive UI
.\run_chainlit.bat

# Run the simple test app
.\run_simple_test.bat
```

## Key Components

The Kern Resources project consists of several key components:

1. **ChainLit UI** - User interface for interacting with the system
2. **CrewAI** - Framework for creating and managing AI agent teams
3. **Novel Memory System** - Four-layer memory system for storing and retrieving information
4. **A2A Protocol** - Protocol for agent-to-agent communication
5. **Model Context Protocol (MCP)** - Protocol for standardized model interactions

## Environment Setup

The project uses an Anaconda environment named `kern_resources_ai_310` with Python 3.10. See the [ChainLit Integration Guide](chainlit_integration_guide.md) for details on setting up the environment.

## Recent Updates

- Fixed ChainLit integration issues (May 2024)
- Updated batch files to use Python module syntax
- Replaced dictionary-based actions with `cl.Action` objects
- Added documentation for A2A and MCP integration

## Contributing

When contributing to the project, please follow these guidelines:

1. Use `cl.Action` objects instead of dictionaries for actions
2. Use Python module syntax to run ChainLit applications
3. Follow A2A and MCP protocols for agent and model interactions
4. Document all changes and additions

## Contact

For questions or issues, please contact Erik Jacobs (erik.jacobs@gmail.com).
