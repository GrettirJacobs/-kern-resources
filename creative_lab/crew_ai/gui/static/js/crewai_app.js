// JavaScript for the memory highlighting system

// Global variables
let currentMemoryId = null;
let currentProtocolName = null;
let currentDocName = null;

// DOM elements
const memoriesList = document.getElementById('memories-list');
const memoryDetails = document.getElementById('memory-details');
const memoryHighlights = document.getElementById('memory-highlights');
const highlightMemoryBtn = document.getElementById('highlight-memory-btn');
const addMemoryBtn = document.getElementById('add-memory-btn');
const saveMemoryBtn = document.getElementById('save-memory-btn');
const saveHighlightBtn = document.getElementById('save-highlight-btn');
const protocolsList = document.getElementById('protocols-list');
const protocolDetails = document.getElementById('protocol-details');
const protocolTask = document.getElementById('protocol-task');
const executeProtocolBtn = document.getElementById('execute-protocol-btn');
const protocolResult = document.getElementById('protocol-result');
const docsList = document.getElementById('docs-list');
const docsDetails = document.getElementById('docs-details');

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    // Load memories
    loadMemories();
    
    // Load protocols
    loadProtocols();
    
    // Load documentation
    loadDocs();
    
    // Set up event listeners
    addMemoryBtn.addEventListener('click', showAddMemoryModal);
    saveMemoryBtn.addEventListener('click', saveMemory);
    highlightMemoryBtn.addEventListener('click', showHighlightMemoryModal);
    saveHighlightBtn.addEventListener('click', saveHighlight);
    executeProtocolBtn.addEventListener('click', executeProtocol);
    
    // Set up tab navigation
    const tabLinks = document.querySelectorAll('.nav-link');
    tabLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            
            // Remove active class from all tabs
            tabLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked tab
            link.classList.add('active');
            
            // Show the corresponding tab content
            const tabId = link.getAttribute('href');
            const tabContent = document.querySelector(tabId);
            
            // Hide all tab content
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('show', 'active');
            });
            
            // Show the selected tab content
            tabContent.classList.add('show', 'active');
        });
    });
});

// Load memories from the server
function loadMemories() {
    fetch('/memories')
        .then(response => response.json())
        .then(memories => {
            memoriesList.innerHTML = '';
            
            if (memories.length === 0) {
                memoriesList.innerHTML = '<p class="text-muted p-3">No memories found</p>';
                return;
            }
            
            memories.forEach(memory => {
                const item = document.createElement('a');
                item.href = '#';
                item.className = 'list-group-item list-group-item-action';
                item.dataset.id = memory.id;
                item.textContent = memory.content.substring(0, 50) + (memory.content.length > 50 ? '...' : '');
                
                item.addEventListener('click', (event) => {
                    event.preventDefault();
                    
                    // Remove active class from all items
                    memoriesList.querySelectorAll('.list-group-item').forEach(i => {
                        i.classList.remove('active');
                    });
                    
                    // Add active class to clicked item
                    item.classList.add('active');
                    
                    // Load memory details
                    loadMemoryDetails(memory.id);
                });
                
                memoriesList.appendChild(item);
            });
        })
        .catch(error => {
            console.error('Error loading memories:', error);
            memoriesList.innerHTML = '<p class="text-danger p-3">Error loading memories</p>';
        });
}

// Load memory details from the server
function loadMemoryDetails(memoryId) {
    fetch(`/memories/${memoryId}`)
        .then(response => response.json())
        .then(memory => {
            currentMemoryId = memory.id;
            
            // Enable the highlight button
            highlightMemoryBtn.disabled = false;
            
            // Display memory details
            memoryDetails.innerHTML = `
                <h5>Memory</h5>
                <div class="memory-content">${memory.content}</div>
                <div class="memory-metadata">
                    <p><strong>ID:</strong> ${memory.id}</p>
                    <p><strong>Source:</strong> ${memory.source}</p>
                    <p><strong>Created:</strong> ${new Date(memory.created_at).toLocaleString()}</p>
                    <p><strong>Metadata:</strong></p>
                    <pre>${JSON.stringify(memory.metadata, null, 2)}</pre>
                </div>
            `;
            
            // Load memory highlights
            loadMemoryHighlights(memory.id);
        })
        .catch(error => {
            console.error('Error loading memory details:', error);
            memoryDetails.innerHTML = '<p class="text-danger">Error loading memory details</p>';
        });
}

// Load memory highlights from the server
function loadMemoryHighlights(memoryId) {
    fetch(`/memories/${memoryId}/highlights`)
        .then(response => response.json())
        .then(highlights => {
            memoryHighlights.innerHTML = '<h5>Highlights</h5>';
            
            if (highlights.length === 0) {
                memoryHighlights.innerHTML += '<p class="text-muted">No highlights found</p>';
                return;
            }
            
            highlights.forEach(highlight => {
                const highlightElement = document.createElement('div');
                highlightElement.className = `highlight highlight-${highlight.metadata.importance || 'medium'}`;
                highlightElement.innerHTML = `
                    <p>${highlight.text}</p>
                    <div class="memory-metadata">
                        <p><strong>Source:</strong> ${highlight.source}</p>
                        <p><strong>Created:</strong> ${new Date(highlight.created_at).toLocaleString()}</p>
                        <p><strong>Importance:</strong> ${highlight.metadata.importance || 'medium'}</p>
                    </div>
                `;
                
                memoryHighlights.appendChild(highlightElement);
            });
        })
        .catch(error => {
            console.error('Error loading memory highlights:', error);
            memoryHighlights.innerHTML = '<p class="text-danger">Error loading memory highlights</p>';
        });
}

// Show the add memory modal
function showAddMemoryModal() {
    const modal = new bootstrap.Modal(document.getElementById('add-memory-modal'));
    modal.show();
}

// Save a new memory
function saveMemory() {
    const content = document.getElementById('memory-content').value;
    const source = document.getElementById('memory-source').value;
    let metadata = {};
    
    try {
        metadata = JSON.parse(document.getElementById('memory-metadata').value);
    } catch (error) {
        alert('Invalid JSON in metadata field');
        return;
    }
    
    if (!content) {
        alert('Content is required');
        return;
    }
    
    fetch('/memories', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content,
            source,
            metadata
        })
    })
        .then(response => response.json())
        .then(data => {
            // Close the modal
            bootstrap.Modal.getInstance(document.getElementById('add-memory-modal')).hide();
            
            // Clear the form
            document.getElementById('memory-content').value = '';
            document.getElementById('memory-source').value = 'user';
            document.getElementById('memory-metadata').value = '{}';
            
            // Reload memories
            loadMemories();
        })
        .catch(error => {
            console.error('Error saving memory:', error);
            alert('Error saving memory');
        });
}

// Show the highlight memory modal
function showHighlightMemoryModal() {
    if (!currentMemoryId) {
        alert('Please select a memory first');
        return;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('highlight-memory-modal'));
    modal.show();
}

// Save a new highlight
function saveHighlight() {
    if (!currentMemoryId) {
        alert('Please select a memory first');
        return;
    }
    
    const text = document.getElementById('highlight-text').value;
    const importance = document.getElementById('highlight-importance').value;
    const source = document.getElementById('highlight-source').value;
    let metadata = {};
    
    try {
        metadata = JSON.parse(document.getElementById('highlight-metadata').value);
    } catch (error) {
        alert('Invalid JSON in metadata field');
        return;
    }
    
    if (!text) {
        alert('Text is required');
        return;
    }
    
    // Add importance to metadata
    metadata.importance = importance;
    
    fetch(`/memories/${currentMemoryId}/highlight`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            highlights: [text],
            source,
            metadata
        })
    })
        .then(response => response.json())
        .then(data => {
            // Close the modal
            bootstrap.Modal.getInstance(document.getElementById('highlight-memory-modal')).hide();
            
            // Clear the form
            document.getElementById('highlight-text').value = '';
            document.getElementById('highlight-importance').value = 'medium';
            document.getElementById('highlight-source').value = 'user';
            document.getElementById('highlight-metadata').value = '{}';
            
            // Reload memory highlights
            loadMemoryHighlights(currentMemoryId);
        })
        .catch(error => {
            console.error('Error saving highlight:', error);
            alert('Error saving highlight');
        });
}

// Load protocols from the server
function loadProtocols() {
    fetch('/protocols')
        .then(response => response.json())
        .then(protocols => {
            protocolsList.innerHTML = '';
            
            if (Object.keys(protocols).length === 0) {
                protocolsList.innerHTML = '<p class="text-muted p-3">No protocols found</p>';
                return;
            }
            
            for (const [name, protocol] of Object.entries(protocols)) {
                const item = document.createElement('a');
                item.href = '#';
                item.className = 'list-group-item list-group-item-action';
                item.dataset.name = name;
                item.textContent = name;
                
                item.addEventListener('click', (event) => {
                    event.preventDefault();
                    
                    // Remove active class from all items
                    protocolsList.querySelectorAll('.list-group-item').forEach(i => {
                        i.classList.remove('active');
                    });
                    
                    // Add active class to clicked item
                    item.classList.add('active');
                    
                    // Load protocol details
                    loadProtocolDetails(name, protocol);
                });
                
                protocolsList.appendChild(item);
            }
        })
        .catch(error => {
            console.error('Error loading protocols:', error);
            protocolsList.innerHTML = '<p class="text-danger p-3">Error loading protocols</p>';
        });
}

// Load protocol details
function loadProtocolDetails(name, protocol) {
    currentProtocolName = name;
    
    // Enable the task input and execute button
    protocolTask.disabled = false;
    executeProtocolBtn.disabled = false;
    
    // Display protocol details
    protocolDetails.innerHTML = `
        <h5>${name}</h5>
        <div class="protocol-metadata">
            <p><strong>Type:</strong> ${protocol.type}</p>
            <p><strong>Capabilities:</strong></p>
            <pre>${JSON.stringify(protocol.capabilities, null, 2)}</pre>
            <p><strong>Metadata:</strong></p>
            <pre>${JSON.stringify(protocol.metadata, null, 2)}</pre>
        </div>
    `;
}

// Execute a protocol task
function executeProtocol() {
    if (!currentProtocolName) {
        alert('Please select a protocol first');
        return;
    }
    
    const task = protocolTask.value;
    
    if (!task) {
        alert('Task is required');
        return;
    }
    
    // Disable the execute button
    executeProtocolBtn.disabled = true;
    executeProtocolBtn.textContent = 'Executing...';
    
    fetch(`/protocols/${currentProtocolName}/execute`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            task
        })
    })
        .then(response => response.json())
        .then(data => {
            // Enable the execute button
            executeProtocolBtn.disabled = false;
            executeProtocolBtn.textContent = 'Execute Task';
            
            // Display the result
            protocolResult.textContent = data.result;
        })
        .catch(error => {
            console.error('Error executing protocol:', error);
            alert('Error executing protocol');
            
            // Enable the execute button
            executeProtocolBtn.disabled = false;
            executeProtocolBtn.textContent = 'Execute Task';
        });
}

// Load documentation from the server
function loadDocs() {
    fetch('/docs')
        .then(response => response.json())
        .then(docs => {
            docsList.innerHTML = '';
            
            if (Object.keys(docs).length === 0) {
                docsList.innerHTML = '<p class="text-muted p-3">No documentation found</p>';
                return;
            }
            
            for (const [name, doc] of Object.entries(docs)) {
                const item = document.createElement('a');
                item.href = '#';
                item.className = 'list-group-item list-group-item-action';
                item.dataset.name = name;
                item.textContent = name;
                
                item.addEventListener('click', (event) => {
                    event.preventDefault();
                    
                    // Remove active class from all items
                    docsList.querySelectorAll('.list-group-item').forEach(i => {
                        i.classList.remove('active');
                    });
                    
                    // Add active class to clicked item
                    item.classList.add('active');
                    
                    // Load documentation details
                    loadDocDetails(name, doc);
                });
                
                docsList.appendChild(item);
            }
        })
        .catch(error => {
            console.error('Error loading documentation:', error);
            docsList.innerHTML = '<p class="text-danger p-3">Error loading documentation</p>';
        });
}

// Load documentation details
function loadDocDetails(name, doc) {
    currentDocName = name;
    
    // Display documentation details
    docsDetails.innerHTML = `
        <h5>${name}</h5>
        <div class="docs-content">
            <pre>${JSON.stringify(doc, null, 2)}</pre>
        </div>
    `;
}
