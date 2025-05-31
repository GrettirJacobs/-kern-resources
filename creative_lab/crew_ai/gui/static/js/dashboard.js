/**
 * Dashboard functionality for CrewAI GUI
 *
 * This file contains the JavaScript code for the dashboard functionality,
 * including status updates, model information, and quick start buttons.
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the dashboard
    initializeDashboard();

    // Set up event listeners
    setupEventListeners();
});

/**
 * Initialize the dashboard by loading status and model information
 */
function initializeDashboard() {
    // Load system status
    loadSystemStatus();

    // Load available models
    loadAvailableModels();
}

/**
 * Set up event listeners for dashboard elements
 */
function setupEventListeners() {
    // Refresh status button
    const refreshStatusBtn = document.getElementById('refresh-status');
    if (refreshStatusBtn) {
        refreshStatusBtn.addEventListener('click', function() {
            loadSystemStatus();
            loadAvailableModels();
        });
    }

    // Refresh results button
    const refreshResultsBtn = document.getElementById('refresh-results');
    if (refreshResultsBtn) {
        refreshResultsBtn.addEventListener('click', function() {
            loadDevelopmentPlans();
        });
    }

    // Run development plan button
    const runDevelopmentPlanBtn = document.getElementById('run-development-plan');
    if (runDevelopmentPlanBtn) {
        runDevelopmentPlanBtn.addEventListener('click', function() {
            runDevelopmentPlan();
        });
    }

    // Quick start buttons
    setupQuickStartButtons();

    // Settings form
    setupSettingsForm();

    // Agent, Task, and Crew creation buttons
    setupCreationButtons();

    // Load development plans
    loadDevelopmentPlans();
}

/**
 * Load system status from the API
 */
function loadSystemStatus() {
    // Show loading indicators
    updateStatusIndicator('crewai-status', 'Loading...', 'bg-secondary');
    updateStatusIndicator('integration-status', 'Loading...', 'bg-secondary');
    updateStatusIndicator('env-manager-status', 'Loading...', 'bg-secondary');

    // Fetch status from the API
    fetch('/api/status')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update status indicators
            updateStatusIndicator(
                'crewai-status',
                data.crewai_available ? 'Available' : 'Not Available',
                data.crewai_available ? 'bg-success' : 'bg-danger'
            );

            updateStatusIndicator(
                'integration-status',
                data.integration_available ? 'Available' : 'Not Available',
                data.integration_available ? 'bg-success' : 'bg-danger'
            );

            updateStatusIndicator(
                'env-manager-status',
                data.env_manager_available ? 'Available' : 'Not Available',
                data.env_manager_available ? 'bg-success' : 'bg-danger'
            );
        })
        .catch(error => {
            console.error('Error fetching system status:', error);

            // Update status indicators to show error
            updateStatusIndicator('crewai-status', 'Error', 'bg-danger');
            updateStatusIndicator('integration-status', 'Error', 'bg-danger');
            updateStatusIndicator('env-manager-status', 'Error', 'bg-danger');
        });
}

/**
 * Load available models from the API
 */
function loadAvailableModels() {
    // Show loading indicators
    updateModelIndicator('openai-model', 'Loading...', 'bg-secondary');
    updateModelIndicator('anthropic-model', 'Loading...', 'bg-secondary');
    updateModelIndicator('groq-model', 'Loading...', 'bg-secondary');
    updateModelIndicator('google-model', 'Loading...', 'bg-secondary');

    // Fetch models from the API
    fetch('/api/models')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update model indicators
            updateModelIndicator(
                'openai-model',
                data.openai || 'Not Configured',
                data.openai ? 'bg-primary' : 'bg-warning'
            );

            updateModelIndicator(
                'anthropic-model',
                data.anthropic || 'Not Configured',
                data.anthropic ? 'bg-primary' : 'bg-warning'
            );

            updateModelIndicator(
                'groq-model',
                data.groq || 'Not Configured',
                data.groq ? 'bg-primary' : 'bg-warning'
            );

            updateModelIndicator(
                'google-model',
                data.google || 'Not Configured',
                data.google ? 'bg-primary' : 'bg-warning'
            );
        })
        .catch(error => {
            console.error('Error fetching available models:', error);

            // Update model indicators to show error
            updateModelIndicator('openai-model', 'Error', 'bg-danger');
            updateModelIndicator('anthropic-model', 'Error', 'bg-danger');
            updateModelIndicator('groq-model', 'Error', 'bg-danger');
            updateModelIndicator('google-model', 'Error', 'bg-danger');
        });
}

/**
 * Update a status indicator with the given text and class
 */
function updateStatusIndicator(elementId, text, className) {
    const element = document.getElementById(elementId);
    if (element) {
        // Remove all background classes
        element.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-secondary', 'bg-primary');

        // Add the new class
        element.classList.add(className);

        // Update the text
        element.textContent = text;
    }
}

/**
 * Update a model indicator with the given text and class
 */
function updateModelIndicator(elementId, text, className) {
    const element = document.getElementById(elementId);
    if (element) {
        // Remove all background classes
        element.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-secondary', 'bg-primary');

        // Add the new class
        element.classList.add(className);

        // Update the text
        element.textContent = text;
    }
}

/**
 * Set up event listeners for quick start buttons
 */
function setupQuickStartButtons() {
    // Create Agent button
    const createAgentBtn = document.querySelector('.card-body button[data-bs-target="#agents"]');
    if (createAgentBtn) {
        createAgentBtn.addEventListener('click', function() {
            // Show the agents tab
            const agentsTab = document.querySelector('a[data-bs-target="#agents"]');
            if (agentsTab) {
                agentsTab.click();

                // Show the create agent modal after a short delay
                setTimeout(function() {
                    const createAgentModal = new bootstrap.Modal(document.getElementById('create-agent-modal'));
                    createAgentModal.show();
                }, 500);
            }
        });
    }

    // Create Task button
    const createTaskBtn = document.querySelector('.card-body button[data-bs-target="#tasks"]');
    if (createTaskBtn) {
        createTaskBtn.addEventListener('click', function() {
            // Show the tasks tab
            const tasksTab = document.querySelector('a[data-bs-target="#tasks"]');
            if (tasksTab) {
                tasksTab.click();

                // Show the create task modal after a short delay
                setTimeout(function() {
                    const createTaskModal = new bootstrap.Modal(document.getElementById('create-task-modal'));
                    createTaskModal.show();
                }, 500);
            }
        });
    }

    // Create Crew button
    const createCrewBtn = document.querySelector('.card-body button[data-bs-target="#crews"]');
    if (createCrewBtn) {
        createCrewBtn.addEventListener('click', function() {
            // Show the crews tab
            const crewsTab = document.querySelector('a[data-bs-target="#crews"]');
            if (crewsTab) {
                crewsTab.click();

                // Show the create crew modal after a short delay
                setTimeout(function() {
                    const createCrewModal = new bootstrap.Modal(document.getElementById('create-crew-modal'));
                    createCrewModal.show();
                }, 500);
            }
        });
    }
}

/**
 * Set up event listeners for the settings form
 */
function setupSettingsForm() {
    // Save settings button
    const saveSettingsBtn = document.getElementById('save-settings');
    if (saveSettingsBtn) {
        saveSettingsBtn.addEventListener('click', function() {
            saveSettings();
        });
    }

    // Temperature range input
    const temperatureInput = document.getElementById('default-temperature');
    const temperatureValue = document.getElementById('temperature-value');
    if (temperatureInput && temperatureValue) {
        temperatureInput.addEventListener('input', function() {
            temperatureValue.textContent = temperatureInput.value;
        });
    }

    // Load API keys from local storage
    loadApiKeys();
}

/**
 * Load API keys from local storage and server
 */
function loadApiKeys() {
    // First try to load from local storage
    loadApiKeysFromLocalStorage();

    // Then try to load from server
    loadApiKeysFromServer();
}

/**
 * Load API keys from local storage
 */
function loadApiKeysFromLocalStorage() {
    // OpenAI API key
    const openaiApiKey = localStorage.getItem('openai-api-key');
    if (openaiApiKey) {
        const openaiApiKeyInput = document.getElementById('openai-api-key');
        if (openaiApiKeyInput) {
            openaiApiKeyInput.value = openaiApiKey;
        }
    }

    // Anthropic API key
    const anthropicApiKey = localStorage.getItem('anthropic-api-key');
    if (anthropicApiKey) {
        const anthropicApiKeyInput = document.getElementById('anthropic-api-key');
        if (anthropicApiKeyInput) {
            anthropicApiKeyInput.value = anthropicApiKey;
        }
    }

    // Groq API key
    const groqApiKey = localStorage.getItem('groq-api-key');
    if (groqApiKey) {
        const groqApiKeyInput = document.getElementById('groq-api-key');
        if (groqApiKeyInput) {
            groqApiKeyInput.value = groqApiKey;
        }
    }

    // Google API key
    const googleApiKey = localStorage.getItem('google-api-key');
    if (googleApiKey) {
        const googleApiKeyInput = document.getElementById('google-api-key');
        if (googleApiKeyInput) {
            googleApiKeyInput.value = googleApiKey;
        }
    }
}

/**
 * Load API keys from server
 */
function loadApiKeysFromServer() {
    fetch('/api/api-keys')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'available') {
                // Update status indicators to show API keys are available
                const apiKeys = data.api_keys;

                // Update status indicators
                updateApiKeyStatus('openai-status', apiKeys.openai ? 'Available' : 'Not Available',
                                  apiKeys.openai ? 'bg-success' : 'bg-danger');
                updateApiKeyStatus('anthropic-status', apiKeys.anthropic ? 'Available' : 'Not Available',
                                  apiKeys.anthropic ? 'bg-success' : 'bg-danger');
                updateApiKeyStatus('groq-status', apiKeys.groq ? 'Available' : 'Not Available',
                                  apiKeys.groq ? 'bg-success' : 'bg-danger');
                updateApiKeyStatus('google-status', apiKeys.google ? 'Available' : 'Not Available',
                                  apiKeys.google ? 'bg-success' : 'bg-danger');
            }
        })
        .catch(error => {
            console.error('Error fetching API keys:', error);
        });
}

/**
 * Update API key status indicator
 */
function updateApiKeyStatus(elementId, text, className) {
    const element = document.getElementById(elementId);
    if (element) {
        // Remove all background classes
        element.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-secondary', 'bg-primary');

        // Add the new class
        element.classList.add(className);

        // Update the text
        element.textContent = text;
    }
}

/**
 * Save settings to local storage and update the server
 */
function saveSettings() {
    // Get API keys
    const openaiApiKey = document.getElementById('openai-api-key').value;
    const anthropicApiKey = document.getElementById('anthropic-api-key').value;
    const groqApiKey = document.getElementById('groq-api-key').value;
    const googleApiKey = document.getElementById('google-api-key').value;

    // Save API keys to local storage
    if (openaiApiKey) {
        localStorage.setItem('openai-api-key', openaiApiKey);
    }

    if (anthropicApiKey) {
        localStorage.setItem('anthropic-api-key', anthropicApiKey);
    }

    if (groqApiKey) {
        localStorage.setItem('groq-api-key', groqApiKey);
    }

    if (googleApiKey) {
        localStorage.setItem('google-api-key', googleApiKey);
    }

    // Get default settings
    const defaultModel = document.getElementById('default-model').value;
    const defaultTemperature = document.getElementById('default-temperature').value;
    const defaultMaxTokens = document.getElementById('default-max-tokens').value;
    const defaultProcess = document.getElementById('default-process').value;

    // Save default settings to local storage
    localStorage.setItem('default-model', defaultModel);
    localStorage.setItem('default-temperature', defaultTemperature);
    localStorage.setItem('default-max-tokens', defaultMaxTokens);
    localStorage.setItem('default-process', defaultProcess);

    // Update API keys on the server
    updateApiKeys({
        openai: openaiApiKey,
        anthropic: anthropicApiKey,
        groq: groqApiKey,
        google: googleApiKey
    });

    // Update settings on the server
    updateSettings({
        models: {
            openai: defaultModel,
            anthropic: defaultModel,
            groq: defaultModel,
            google: defaultModel
        },
        temperature: defaultTemperature,
        max_tokens: defaultMaxTokens,
        process: defaultProcess
    });

    // Show success message
    alert('Settings saved successfully!');

    // Reload system status and available models
    loadSystemStatus();
    loadAvailableModels();
}

/**
 * Update API keys on the server
 */
function updateApiKeys(apiKeys) {
    fetch('/api/api-keys', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            api_keys: {
                openai: apiKeys.openai,
                anthropic: apiKeys.anthropic,
                groq: apiKeys.groq,
                google: apiKeys.google
            }
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('API keys updated:', data);

        // Check for any failed updates
        if (data.results) {
            let failedUpdates = [];
            for (const [provider, status] of Object.entries(data.results)) {
                if (status === 'failed' || status === 'invalid') {
                    failedUpdates.push(provider);
                }
            }

            if (failedUpdates.length > 0) {
                const failedProviders = failedUpdates.join(', ');
                showError(`Failed to update API keys for: ${failedProviders}. Please check the format of your API keys.`);
            }
        }
    })
    .catch(error => {
        console.error('Error updating API keys:', error);
        showError('Error updating API keys. Please try again.');
    });
}

/**
 * Show an error message to the user
 */
function showError(message) {
    // Check if there's an error container in the settings tab
    let errorContainer = document.getElementById('settings-error');

    // If not, create one
    if (!errorContainer) {
        const settingsTab = document.getElementById('settings');
        if (settingsTab) {
            errorContainer = document.createElement('div');
            errorContainer.id = 'settings-error';
            errorContainer.className = 'alert alert-danger mt-3';
            settingsTab.prepend(errorContainer);
        }
    }

    // Show the error message
    if (errorContainer) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';

        // Hide the error after 5 seconds
        setTimeout(() => {
            errorContainer.style.display = 'none';
        }, 5000);
    } else {
        // Fallback to alert if we can't find or create the error container
        alert(message);
    }
}

/**
 * Update settings on the server
 */
function updateSettings(settings) {
    fetch('/api/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Settings updated:', data);
        if (data.status !== 'saved') {
            showError('Failed to save settings. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error updating settings:', error);
        showError('Error updating settings. Please try again.');
    });
}

/**
 * Set up event listeners for agent, task, and crew creation buttons
 */
function setupCreationButtons() {
    console.log('setupCreationButtons function called');

    // Create Agent button
    const createAgentBtn = document.getElementById('create-agent-btn');
    console.log('createAgentBtn:', createAgentBtn);
    if (createAgentBtn) {
        console.log('Adding event listener to createAgentBtn');
        createAgentBtn.addEventListener('click', function() {
            console.log('createAgentBtn clicked');
            createAgent();
        });
    }

    // Create Task button
    const createTaskBtn = document.getElementById('create-task-btn');
    console.log('createTaskBtn:', createTaskBtn);
    if (createTaskBtn) {
        console.log('Adding event listener to createTaskBtn');
        createTaskBtn.addEventListener('click', function() {
            console.log('createTaskBtn clicked');
            createTask();
        });
    }

    // Create Crew button
    const createCrewBtn = document.getElementById('create-crew-btn');
    console.log('createCrewBtn:', createCrewBtn);
    if (createCrewBtn) {
        console.log('Adding event listener to createCrewBtn');
        createCrewBtn.addEventListener('click', function() {
            console.log('createCrewBtn clicked');
            createCrew();
        });
    }
}

/**
 * Create a new agent
 */
function createAgent() {
    console.log('createAgent function called');

    // Get form data
    const role = document.getElementById('agent-role').value;
    const goal = document.getElementById('agent-goal').value;
    const backstory = document.getElementById('agent-backstory').value;
    const model = document.getElementById('agent-model').value;
    const verbose = document.getElementById('agent-verbose').checked;
    const allowDelegation = document.getElementById('agent-allow-delegation').checked;

    console.log('Form data:', { role, goal, backstory, model, verbose, allowDelegation });

    // Validate form data
    if (!role) {
        showError('Role is required');
        return;
    }

    if (!goal) {
        showError('Goal is required');
        return;
    }

    // Prepare data for the server
    const data = {
        role: role,
        goal: goal,
        backstory: backstory || 'You are an AI agent.',
        verbose: verbose,
        allow_delegation: allowDelegation,
        llm_config: {
            provider: model,
            model: null,  // Use default model for the provider
            temperature: 0.7  // Use default temperature
        }
    };

    console.log('Sending data to server:', data);

    // Send data to the server
    fetch('/api/agents', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Agent created:', data);

        // Close the modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('create-agent-modal'));
        if (modal) {
            modal.hide();
        }

        // Show success message
        alert('Agent created successfully!');

        // Clear the form
        document.getElementById('agent-role').value = '';
        document.getElementById('agent-goal').value = '';
        document.getElementById('agent-backstory').value = '';
        document.getElementById('agent-model').value = 'groq';
        document.getElementById('agent-verbose').checked = true;
        document.getElementById('agent-allow-delegation').checked = false;

        // Reload agents table
        loadAgents();
    })
    .catch(error => {
        console.error('Error creating agent:', error);
        showError('Error creating agent. Please try again.');
    });
}

/**
 * Create a new task
 */
function createTask() {
    // TODO: Implement task creation
    alert('Task creation not implemented yet.');
}

/**
 * Create a new crew
 */
function createCrew() {
    // TODO: Implement crew creation
    alert('Crew creation not implemented yet.');
}

/**
 * Load agents from the server
 */
function loadAgents() {
    fetch('/api/agents')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update agents table
            const agentsTable = document.getElementById('agents-table');
            if (agentsTable) {
                agentsTable.innerHTML = '';

                if (Object.keys(data).length === 0) {
                    agentsTable.innerHTML = '<tr><td colspan="5" class="text-center">No agents found</td></tr>';
                    return;
                }

                for (const [id, agent] of Object.entries(data)) {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${id}</td>
                        <td>${agent.role}</td>
                        <td>${agent.goal}</td>
                        <td>${agent.llm_config?.provider || 'Default'}</td>
                        <td>
                            <button class="btn btn-sm btn-danger" onclick="deleteAgent('${id}')">Delete</button>
                        </td>
                    `;
                    agentsTable.appendChild(row);
                }
            }
        })
        .catch(error => {
            console.error('Error loading agents:', error);
            const agentsTable = document.getElementById('agents-table');
            if (agentsTable) {
                agentsTable.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error loading agents</td></tr>';
            }
        });
}

/**
 * Delete an agent
 */
function deleteAgent(id) {
    if (confirm(`Are you sure you want to delete agent ${id}?`)) {
        fetch(`/api/agents/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Agent deleted:', data);

            // Show success message
            alert('Agent deleted successfully!');

            // Reload agents table
            loadAgents();
        })
        .catch(error => {
            console.error('Error deleting agent:', error);
            showError('Error deleting agent. Please try again.');
        });
    }
}

/**
 * Load development plans from the server
 */
function loadDevelopmentPlans() {
    fetch('/api/development-plans')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update results accordion
            const resultsAccordion = document.getElementById('results-accordion');
            if (resultsAccordion) {
                resultsAccordion.innerHTML = '';

                if (data.length === 0) {
                    resultsAccordion.innerHTML = '<div class="alert alert-info">No development plans found</div>';
                    return;
                }

                for (const plan of data) {
                    const accordionItem = document.createElement('div');
                    accordionItem.className = 'accordion-item';
                    accordionItem.innerHTML = `
                        <h2 class="accordion-header" id="heading-${plan.id}">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${plan.id}" aria-expanded="false" aria-controls="collapse-${plan.id}">
                                ${plan.title} <span class="badge bg-secondary ms-2">${plan.created_date}</span>
                            </button>
                        </h2>
                        <div id="collapse-${plan.id}" class="accordion-collapse collapse" aria-labelledby="heading-${plan.id}" data-bs-parent="#results-accordion">
                            <div class="accordion-body">
                                <div class="text-center">
                                    <div class="spinner-border" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    resultsAccordion.appendChild(accordionItem);

                    // Add event listener to load content when expanded
                    const collapseElement = accordionItem.querySelector(`#collapse-${plan.id}`);
                    collapseElement.addEventListener('shown.bs.collapse', function() {
                        loadDevelopmentPlanContent(plan.id, collapseElement.querySelector('.accordion-body'));
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error loading development plans:', error);
            const resultsAccordion = document.getElementById('results-accordion');
            if (resultsAccordion) {
                resultsAccordion.innerHTML = '<div class="alert alert-danger">Error loading development plans</div>';
            }
        });
}

/**
 * Load development plan content from the server
 */
function loadDevelopmentPlanContent(planId, container) {
    fetch(`/api/development-plans/${planId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Convert markdown to HTML
            const converter = new showdown.Converter();
            const html = converter.makeHtml(data.content);

            // Update container
            container.innerHTML = `
                <div class="markdown-content">
                    ${html}
                </div>
                <div class="mt-3">
                    <button class="btn btn-sm btn-primary" onclick="viewFullDevelopmentPlan('${planId}')">
                        <i class="bi bi-arrows-fullscreen"></i> View Full Report
                    </button>
                </div>
            `;
        })
        .catch(error => {
            console.error(`Error loading development plan content for ${planId}:`, error);
            container.innerHTML = '<div class="alert alert-danger">Error loading development plan content</div>';
        });
}

/**
 * View full development plan in a modal
 */
function viewFullDevelopmentPlan(planId) {
    fetch(`/api/development-plans/${planId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update modal
            const modalTitle = document.getElementById('view-result-modal-label');
            const modalContent = document.getElementById('result-content');

            if (modalTitle && modalContent) {
                modalTitle.textContent = 'Development Plan';
                modalContent.textContent = data.content;

                // Show modal
                const modal = new bootstrap.Modal(document.getElementById('view-result-modal'));
                modal.show();

                // Set up copy button
                const copyBtn = document.getElementById('copy-result-btn');
                if (copyBtn) {
                    copyBtn.onclick = function() {
                        navigator.clipboard.writeText(data.content)
                            .then(() => {
                                alert('Development plan copied to clipboard!');
                            })
                            .catch(err => {
                                console.error('Error copying to clipboard:', err);
                                alert('Failed to copy development plan to clipboard');
                            });
                    };
                }
            }
        })
        .catch(error => {
            console.error(`Error loading full development plan for ${planId}:`, error);
            alert('Error loading full development plan');
        });
}

/**
 * Run the development plan process
 */
function runDevelopmentPlan() {
    if (confirm('Are you sure you want to run the development plan process? This may take several minutes.')) {
        fetch('/api/run-development-plan', {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert('Development plan process started. This may take several minutes. The results will appear in the Results tab when complete.');
        })
        .catch(error => {
            console.error('Error running development plan process:', error);
            alert('Error running development plan process');
        });
    }
}

// Initialize the dashboard when the page loads
initializeDashboard();

// Load agents when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Load agents
    loadAgents();

    // Add direct event listener to the create agent button
    const createAgentBtn = document.getElementById('create-agent-btn');
    if (createAgentBtn) {
        console.log('Adding direct event listener to createAgentBtn');
        createAgentBtn.onclick = function() {
            console.log('createAgentBtn clicked directly');
            createAgent();
        };
    } else {
        console.log('createAgentBtn not found in DOMContentLoaded');
    }
});
