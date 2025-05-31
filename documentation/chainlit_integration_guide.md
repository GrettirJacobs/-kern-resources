# ChainLit Integration Guide

This document provides guidance on integrating ChainLit with the Kern Resources project, including best practices, common issues, and solutions.

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [Running ChainLit Applications](#running-chainlit-applications)
3. [Action Handling](#action-handling)
4. [API Integration](#api-integration)
5. [Common Issues and Solutions](#common-issues-and-solutions)
6. [Testing](#testing)

## Environment Setup

### Anaconda Environment

The Kern Resources project uses an Anaconda environment named `kern_resources_ai_310` with Python 3.10:

```bash
# Activate the environment
conda activate kern_resources_ai_310

# If you need to create the environment
conda create -n kern_resources_ai_310 python=3.10
conda activate kern_resources_ai_310
```

### Required Packages

The following packages are required for ChainLit integration:

```bash
# Install ChainLit
pip install chainlit==2.5.5

# Install Pydantic (specific version for compatibility)
pip install pydantic==2.10.1

# Install CrewAI
pip install crewai==0.118.0
```

## Running ChainLit Applications

### Best Practices

Always use the Python module syntax to run ChainLit applications:

```bash
python -m chainlit run your_app.py -w --port 8000
```

This bypasses PATH issues and ensures the correct Python environment is used.

### Batch Files

Use batch files to standardize the execution of ChainLit applications:

```batch
@echo off
echo Starting ChainLit Application
echo ===========================
echo.

REM Set the Python path
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Create necessary directories
if not exist mockups mkdir mockups
if not exist reports mkdir reports

echo Activating Anaconda environment...
call C:\Users\ErikzConfuzer\anaconda3\Scripts\activate.bat kern_resources_ai_310

echo Starting ChainLit application...
python -m chainlit run your_app.py -w --port 8000

echo.
echo Press any key to exit...
pause > nul
```

## Action Handling

### Using cl.Action Objects

Always use `cl.Action` objects instead of dictionaries for actions:

```python
# CORRECT: Use cl.Action objects
actions = [
    cl.Action(
        name="action_name", 
        payload={"value": "action_value"}, 
        label="Action Label", 
        tooltip="Action description"
    )
]

# INCORRECT: Don't use dictionaries
actions = [
    {"name": "action_name", "value": "action_value", "label": "Action Label", "description": "Action description"}
]
```

### Action Callbacks

In action callbacks, always use `action.payload.get("value")` to access the action value:

```python
@cl.action_callback("action_name")
async def handle_action(action):
    # CORRECT: Use action.payload.get("value")
    value = action.payload.get("value")
    
    # INCORRECT: Don't use action.value
    # value = action.value
    
    await cl.Message(content=f"Action value: {value}").send()
```

## API Integration

### A2A Integration

The Kern Resources project is integrated with A2A (Agent-to-Agent) protocol. When implementing API integrations, ensure compatibility with A2A.

### Model Context Protocol (MCP)

All API implementations should use the Model Context Protocol (MCP) for standardized communication between components:

1. Use MCP-compatible interfaces for all model interactions
2. Ensure proper context handling according to MCP specifications
3. Maintain compatibility with A2A protocol requirements

### API Key Management

Use environment variables for API keys:

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
```

Ensure the `.env` file is added to `.gitignore` to prevent accidental exposure of API keys.

## Common Issues and Solutions

### 'dict' object has no attribute 'send'

**Issue**: Using dictionaries instead of `cl.Action` objects for actions.

**Solution**: Replace all dictionary-based actions with `cl.Action` objects:

```python
# Before
actions = [{"name": "action_name", "value": "value"}]

# After
actions = [cl.Action(name="action_name", payload={"value": "value"})]
```

### ChainLit Command Not Found

**Issue**: The `chainlit` command is not recognized despite successful installation.

**Solution**: Use Python module syntax instead:

```bash
# Before
chainlit run app.py

# After
python -m chainlit run app.py
```

### Environment Activation Issues

**Issue**: Anaconda environment activation issues in batch files.

**Solution**: Use the full path to the activate script and add `call` before activation commands:

```batch
call C:\Users\ErikzConfuzer\anaconda3\Scripts\activate.bat kern_resources_ai_310
```

## Testing

### Simple Test App

A simple test app is available to verify ChainLit functionality:

```bash
.\run_simple_test.bat
```

This runs `simple_test_app.py`, which tests basic ChainLit features including action handling.

### Comprehensive UI

The comprehensive UI can be tested with:

```bash
.\run_chainlit.bat
```

This runs `comprehensive_ui.py`, which provides a multi-page interface for interacting with CrewAI, viewing reports, and more.

## Conclusion

Following these guidelines will ensure proper integration of ChainLit with the Kern Resources project. Always use `cl.Action` objects for actions, use Python module syntax to run ChainLit applications, and ensure proper environment activation in batch files.
