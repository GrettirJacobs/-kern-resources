# CrewAI GUI JavaScript Files

This directory contains the JavaScript files for the CrewAI GUI.

## Files

- `dashboard.js`: Implements the dashboard functionality for the CrewAI GUI
- `crewai_app.js`: Implements the memory highlighting system (not directly related to CrewAI)

## Dashboard.js

The `dashboard.js` file implements the dashboard functionality for the CrewAI GUI, including:

- System status indicators
- Model information display
- Quick start buttons
- Settings form

### Features

- **System Status**: Shows whether CrewAI, the integration, and the environment manager are available
- **Model Information**: Shows the configured models for each provider (OpenAI, Anthropic, Groq, Google)
- **Quick Start Buttons**: Navigate to the appropriate tabs and open the corresponding modals
- **Settings Form**: Saves API keys and default settings to local storage

### API Calls

The dashboard makes the following API calls:

- `GET /api/status`: Gets the status of the CrewAI integration
- `GET /api/models`: Gets the available models for each provider

### Functions

- `initializeDashboard()`: Initializes the dashboard by loading status and model information
- `setupEventListeners()`: Sets up event listeners for dashboard elements
- `loadSystemStatus()`: Loads system status from the API
- `loadAvailableModels()`: Loads available models from the API
- `updateStatusIndicator()`: Updates a status indicator with the given text and class
- `updateModelIndicator()`: Updates a model indicator with the given text and class
- `setupQuickStartButtons()`: Sets up event listeners for quick start buttons
- `setupSettingsForm()`: Sets up event listeners for the settings form
- `loadApiKeys()`: Loads API keys from local storage
- `saveSettings()`: Saves settings to local storage

## Usage

The dashboard.js file is included in the index.html file and is automatically loaded when the page loads. It initializes the dashboard and sets up event listeners for the various dashboard elements.

## Development

To modify the dashboard functionality, edit the dashboard.js file and restart the server. The changes will be automatically loaded when the page is refreshed.

## Credits

The dashboard.js file was created by the Kern Resources team, with assistance from AI models including Claude 3.7 Sonnet.
