# Instructions for Next Chat

## Project Information Files

For our next chat, please provide the AI assistant with the following files to quickly get up to speed on the Kern Resources project:

### Machine-Readable Project Information

```
documentation/project_info.json
```
or
```
documentation/project_info.yaml
```

### Human-Readable Project Summary

```
documentation/project_summary.md
```

### Latest Session Summary

```
documentation/session_summaries/session_2025_04_20.md
```

These files contain comprehensive information about:
- The purpose of the Kern Resources codebase
- The novel memory system architecture and implementation
- How CrewAI, A2A, and other tools fit into the codebase
- The development history of the project
- Remaining development tasks
- Known challenges
- Current development focus (CrewAI GUI Dashboard Implementation)

## Current Development Focus

We are currently focused on:

1. **Implementing the CrewAI GUI** with full functionality for creating and running AI agent crews
2. **Improving the dashboard functionality** with status updates, model information, and quick start buttons
3. **Implementing agent, task, and crew creation** functionality in the GUI
4. **Adding the ability to run crews and view results** through the GUI

In our last session, we fixed the CrewAI integration to properly detect and use the installed CrewAI package, disabled automatic browser opening in the GUI to prevent multiple tabs from being created, and added dashboard functionality to make the GUI more interactive and useful.

## Next Steps

In our next chat, we should focus on:

1. Implementing the agent creation functionality in the CrewAI GUI
2. Implementing the task creation functionality in the CrewAI GUI
3. Implementing the crew creation functionality in the CrewAI GUI
4. Adding the ability to run crews and view results through the GUI
5. Improving error handling and user feedback in the GUI

## Additional Context

Please also remind the AI assistant of your development preferences:

1. Preference for using tested open source code with MIT or Apache 2.0 licenses
2. Desire to maintain and enhance the novel memory system ideas
3. Openness to suggestions for alternative approaches
4. Practical implementation choices when appropriate
5. Importance of documenting the development process

## Session Summary

For reference, a summary of our current session is available at:

```
documentation/session_summaries/session_2025_04_20.md
```

This file contains details about the tasks completed, key accomplishments, issues encountered, and next steps for the CrewAI GUI implementation.

## Key Files and Locations

### CrewAI GUI Directory Structure

```
creative_lab/crew_ai/gui/
├── templates/         # HTML templates
├── static/            # Static files (CSS, JavaScript)
│   ├── css/           # CSS files
│   └── js/            # JavaScript files
├── crewai_gui.py      # Main GUI module
├── crewai_api.py      # API endpoints
├── crewai_integration.py # CrewAI integration
├── enhanced_env_manager.py # Environment variable manager
└── run_gui.py         # Script to run the GUI
```

### Important Files

- **Main GUI Module**: `creative_lab/crew_ai/gui/crewai_gui.py`
- **API Endpoints**: `creative_lab/crew_ai/gui/crewai_api.py`
- **CrewAI Integration**: `creative_lab/crew_ai/gui/crewai_integration.py`
- **Environment Manager**: `creative_lab/crew_ai/gui/enhanced_env_manager.py`
- **Run Script**: `creative_lab/crew_ai/gui/run_gui.py`
- **HTML Template**: `creative_lab/crew_ai/gui/templates/index.html`
- **Dashboard JavaScript**: `creative_lab/crew_ai/gui/static/js/dashboard.js`
- **LLM Helper**: `creative_lab/crew_ai/llm_helper.py`
- **Environment File**: `creative_lab/crew_ai/.env`
