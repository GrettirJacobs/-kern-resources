# ChainLit Plugin System Documentation

## Overview

The ChainLit Plugin System is a modular, extensible architecture that allows ChainLit to seamlessly integrate with various development tools like CrewAI, VS Code, Windsurf, and online assistants. The system is designed to be scalable, allowing for easy addition of new integrations in the future.

## Architecture

The plugin system consists of the following components:

### 1. Plugin Manager

The Plugin Manager is responsible for:
- Registering and managing plugins
- Routing events to the appropriate handlers
- Rendering UI components provided by plugins

```python
# Example usage of the Plugin Manager
plugin_manager = PluginManager()
plugin_manager.register_plugin("crewai", CrewAIPlugin())
await plugin_manager.trigger_event("run_crewai", {"query": "Analyze this code"})
await plugin_manager.render_ui_component("crewai.crewai_page")
```

### 2. Plugin Base

The Plugin Base is the abstract base class that all plugins must inherit from. It defines the interface that plugins must implement:

```python
class PluginBase:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def get_event_handlers(self):
        """Return a dictionary of event handlers."""
        return {}
    
    def get_ui_components(self):
        """Return UI components provided by this plugin."""
        return {}
    
    def initialize(self):
        """Initialize the plugin."""
        pass
    
    def shutdown(self):
        """Clean up resources when shutting down."""
        pass
```

### 3. Integration Plugins

Integration Plugins are concrete implementations of the Plugin Base that provide specific functionality:

- **CrewAI Plugin**: Integrates CrewAI for agent-based workflows
- **VS Code Plugin**: Integrates VS Code for file editing and management
- **Windsurf Plugin**: Integrates Windsurf for data querying and analysis
- **Online Assistants Plugin**: Integrates online AI assistants for chat-based interactions

### 4. Event System

The Event System allows plugins to respond to events triggered by the UI or other plugins:

```python
# Triggering an event
await plugin_manager.trigger_event("message", {"content": "Hello, world!"})

# Handling an event in a plugin
async def handle_message(self, message_data):
    content = message_data.get("content")
    # Process the message
    return {"status": "success"}
```

### 5. UI Components

UI Components are reusable UI elements provided by plugins that can be rendered by the UI:

```python
# Rendering a UI component
await plugin_manager.render_ui_component("crewai.crewai_page")

# Defining a UI component in a plugin
async def show_crewai_page(self):
    # Show the CrewAI page
    await cl.Message(content="CrewAI Page").send()
    return {"status": "success"}
```

## Plugin Implementations

### CrewAI Plugin

The CrewAI Plugin integrates CrewAI with ChainLit, providing:

- Agent creation and management
- Task definition and execution
- Crew formation and monitoring
- Result analysis and reporting

Key components:
- `crewai_page`: Main interface for CrewAI
- `crew_builder`: Interface for building CrewAI crews
- `agent_designer`: Interface for designing CrewAI agents
- `task_creator`: Interface for creating CrewAI tasks
- `crew_monitor`: Interface for monitoring CrewAI crews

### VS Code Plugin

The VS Code Plugin integrates VS Code with ChainLit, providing:

- File browsing and navigation
- Code viewing and editing
- VS Code integration for advanced editing
- Recent files tracking

Key components:
- `vscode_page`: Main interface for VS Code integration
- `file_browser`: Interface for browsing files and directories
- `code_editor`: Interface for viewing and editing code
- `vscode_launcher`: Interface for launching VS Code

### Windsurf Plugin

The Windsurf Plugin integrates Windsurf with ChainLit, providing:

- Query building and execution
- Query saving and management
- Result viewing and analysis
- Action execution

Key components:
- `windsurf_page`: Main interface for Windsurf
- `windsurf_dashboard`: Dashboard for Windsurf
- `windsurf_query_builder`: Interface for building Windsurf queries
- `windsurf_results_viewer`: Interface for viewing Windsurf query results

### Online Assistants Plugin

The Online Assistants Plugin integrates online AI assistants with ChainLit, providing:

- Chat with multiple AI assistants
- Conversation management
- Assistant settings configuration
- Response comparison

Key components:
- `assistants_page`: Main interface for online assistants
- `assistants_dashboard`: Dashboard for online assistants
- `assistant_chat`: Interface for chatting with an assistant
- `assistant_settings`: Interface for configuring assistant settings

## Adding a New Plugin

To add a new plugin to the system:

1. Create a new Python file in the `plugins` directory
2. Import the `PluginBase` class
3. Create a new class that inherits from `PluginBase`
4. Implement the required methods
5. Register the plugin with the plugin manager

Example:

```python
from .plugin_base import PluginBase
import chainlit as cl

class MyPlugin(PluginBase):
    def __init__(self):
        super().__init__("My Plugin", "Description of my plugin")
    
    def get_event_handlers(self):
        return {
            "my_event": self.handle_my_event
        }
    
    def get_ui_components(self):
        return {
            "my_component": self.show_my_component
        }
    
    async def handle_my_event(self, event_data):
        # Handle the event
        return {"status": "success"}
    
    async def show_my_component(self):
        # Show the UI component
        await cl.Message(content="My Component").send()
        return {"status": "success"}
```

Then register the plugin in `plugin_ui.py`:

```python
from plugins.my_plugin import MyPlugin

# Register the plugin
plugin_manager.register_plugin("my_plugin", MyPlugin())
```

## Running the Plugin-based UI

To run the plugin-based UI, use the `run_plugin_ui.bat` script:

```
.\run_plugin_ui.bat
```

This will start the ChainLit application with the plugin system on port 8005.

## A2A and MCP Integration

The plugin system is designed to work with the Agent-to-Agent (A2A) protocol and Model Context Protocol (MCP):

- **A2A Protocol**: Used for standardized communication between agents
- **MCP**: Used for standardized model interactions

Plugins can implement these protocols to ensure compatibility with the broader ecosystem.
