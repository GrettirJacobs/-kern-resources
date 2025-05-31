# Conversational UI Implementation Plan

## Overview

This document outlines the detailed plan for implementing the conversational AI interface for the Kern Resources memory retrieval system. The conversational interface will complement the existing structured search interface, providing a more natural and intuitive way for users to interact with the memory system.

## Current Status

- ✅ Fixed Flask server issues by starting Qdrant Docker container
- ✅ Implemented HTML/CSS for conversational interface
- ✅ Positioned conversational interface above memory search
- ⏳ Implementing JavaScript functionality for chat interface
- ⏳ Creating backend API endpoint for chat

## Implementation Plan

### 1. Frontend Implementation

#### 1.1 JavaScript Functionality for Chat Interface

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    
    // Conversation history
    let conversationHistory = [];
    
    // Handle send button click
    sendButton.addEventListener('click', function() {
        sendMessage();
    });
    
    // Handle Enter key press
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Function to send message
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message === '') return;
        
        // Display user message
        displayUserMessage(message);
        
        // Add to conversation history
        conversationHistory.push({
            role: 'user',
            content: message
        });
        
        // Clear input
        chatInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send to API
        sendToAPI(message);
    }
    
    // Function to display user message
    function displayUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.innerHTML = `
            <p>${escapeHtml(message)}</p>
            <div class="message-time">${getCurrentTime()}</div>
        `;
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Function to display AI message
    function displayAIMessage(message) {
        // Remove typing indicator if present
        removeTypingIndicator();
        
        const messageElement = document.createElement('div');
        messageElement.className = 'message ai-message';
        messageElement.innerHTML = `
            <p>${escapeHtml(message)}</p>
            <div class="message-time">${getCurrentTime()}</div>
        `;
        chatMessages.appendChild(messageElement);
        scrollToBottom();
        
        // Add to conversation history
        conversationHistory.push({
            role: 'assistant',
            content: message
        });
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.className = 'message ai-message typing-indicator';
        typingElement.innerHTML = `
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        chatMessages.appendChild(typingElement);
        scrollToBottom();
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Function to send message to API
    function sendToAPI(message) {
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: message,
                conversation_history: conversationHistory
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayAIMessage(data.response);
                
                // If search results are included, update the search results section
                if (data.search_results && data.search_results.length > 0) {
                    updateSearchResults(data);
                }
            } else {
                displayAIMessage('I apologize, but I encountered an error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            displayAIMessage('I apologize, but I encountered an error: ' + error.message);
        });
    }
    
    // Function to update search results
    function updateSearchResults(data) {
        // This function will update the search results section with the results from the chat query
        // It will reuse the existing displayResults function from the search interface
        if (typeof displayResults === 'function') {
            displayResults(data, 1);
        }
    }
    
    // Helper function to get current time
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // Helper function to escape HTML
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    
    // Helper function to scroll chat to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
```

#### 1.2 CSS Enhancements for Typing Indicator

```css
.typing-dots {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 20px;
}

.typing-dots span {
    display: inline-block;
    width: 8px;
    height: 8px;
    margin: 0 2px;
    background-color: #6c757d;
    border-radius: 50%;
    opacity: 0.6;
    animation: typing-dot 1.4s infinite ease-in-out both;
}

.typing-dots span:nth-child(1) {
    animation-delay: 0s;
}

.typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typing-dot {
    0%, 80%, 100% {
        transform: scale(0.6);
    }
    40% {
        transform: scale(1);
    }
}
```

### 2. Backend Implementation

#### 2.1 Chat API Endpoint

```python
@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle conversational queries.
    
    Returns:
        JSON response with the AI's reply
    """
    try:
        data = request.json
        query = data.get('query', '')
        conversation_history = data.get('conversation_history', [])
        
        # Analyze query
        query_understanding = QueryUnderstanding()
        query_params = query_understanding.analyze_query(query, conversation_history)
        
        # Perform search based on extracted parameters
        search_results = []
        if query_params.get('search_type') == 'vector':
            search_results = memory_search.vector_search(query_params.get('query'))
        elif query_params.get('search_type') == 'tag':
            search_results = memory_search.tag_search(query_params.get('tags'))
        else:
            search_results = memory_search.dual_search(
                query_params.get('query'),
                tags=query_params.get('tags')
            )
        
        # Generate response
        response_generation = ResponseGeneration()
        response = response_generation.generate_response(
            query,
            search_results,
            conversation_history
        )
        
        return jsonify({
            'success': True,
            'response': response,
            'search_results': search_results,
            'search_type': query_params.get('search_type', 'dual'),
            'query': query_params.get('query', query),
            'total': len(search_results),
            'limit': 10
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
```

#### 2.2 Query Understanding Module

```python
class QueryUnderstanding:
    def __init__(self, openai_api_key=None, anthropic_api_key=None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        # Initialize LLM client based on available API keys
        if self.openai_api_key:
            import openai
            self.client = openai.OpenAI(api_key=self.openai_api_key)
            self.model = "gpt-4o"
        elif self.anthropic_api_key:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.model = "claude-3-opus-20240229"
        else:
            # Fallback to mock implementation
            self.client = None
            self.model = None
        
    def analyze_query(self, query, conversation_history=None):
        """
        Analyze a natural language query to extract search parameters.
        
        Args:
            query: The user's query
            conversation_history: Previous messages in the conversation
            
        Returns:
            Dictionary with extracted parameters
        """
        if not self.client:
            # Mock implementation for testing
            return self._mock_analyze_query(query)
        
        # Prepare conversation for LLM
        messages = []
        
        # System message with instructions
        system_message = """
        You are an AI assistant that analyzes user queries about a memory system.
        Your task is to extract search parameters from natural language queries.
        
        The memory system supports three types of search:
        1. Vector search: Semantic similarity search using embeddings
        2. Tag search: Filtering by specific tags
        3. Dual search: Combination of vector and tag search
        
        Extract the following information:
        - search_type: The type of search to perform (vector, tag, or dual)
        - query: The main search query (for vector or dual search)
        - tags: List of tags to filter by (for tag or dual search)
        - date_range: Optional date range for filtering
        - source: Optional source filter
        
        Return the extracted parameters in a structured format.
        """
        
        messages.append({"role": "system", "content": system_message})
        
        # Add conversation history
        if conversation_history:
            for message in conversation_history[-5:]:  # Include last 5 messages for context
                messages.append({"role": message["role"], "content": message["content"]})
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        # Call LLM API
        if self.openai_api_key:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
        elif self.anthropic_api_key:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=system_message,
                messages=[{"role": m["role"], "content": m["content"]} for m in messages if m["role"] != "system"]
            )
            result = json.loads(response.content[0].text)
        
        # Ensure required fields are present
        if 'search_type' not in result:
            result['search_type'] = 'dual'
        if 'query' not in result and result['search_type'] in ['vector', 'dual']:
            result['query'] = query
        if 'tags' not in result and result['search_type'] in ['tag', 'dual']:
            result['tags'] = []
        
        return result
    
    def _mock_analyze_query(self, query):
        """Mock implementation for testing without API keys"""
        query_lower = query.lower()
        
        # Default to dual search
        search_type = 'dual'
        tags = []
        
        # Check for explicit search type mentions
        if 'vector search' in query_lower or 'semantic search' in query_lower:
            search_type = 'vector'
        elif 'tag search' in query_lower or 'filter by tag' in query_lower:
            search_type = 'tag'
        
        # Extract potential tags (simple implementation)
        tag_indicators = ['tag:', 'category:', 'type:', 'location:']
        for indicator in tag_indicators:
            if indicator in query_lower:
                parts = query_lower.split(indicator)
                if len(parts) > 1:
                    tag_value = parts[1].split()[0].strip()
                    tag_type = indicator.replace(':', '')
                    tags.append({'type': tag_type, 'value': tag_value})
        
        return {
            'search_type': search_type,
            'query': query,
            'tags': tags
        }
```

#### 2.3 Response Generation Module

```python
class ResponseGeneration:
    def __init__(self, openai_api_key=None, anthropic_api_key=None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        # Initialize LLM client based on available API keys
        if self.openai_api_key:
            import openai
            self.client = openai.OpenAI(api_key=self.openai_api_key)
            self.model = "gpt-4o"
        elif self.anthropic_api_key:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.model = "claude-3-opus-20240229"
        else:
            # Fallback to mock implementation
            self.client = None
            self.model = None
        
    def generate_response(self, query, search_results, conversation_history=None):
        """
        Generate a natural language response based on search results.
        
        Args:
            query: The user's query
            search_results: Results from the memory search
            conversation_history: Previous messages in the conversation
            
        Returns:
            Natural language response
        """
        if not self.client:
            # Mock implementation for testing
            return self._mock_generate_response(query, search_results)
        
        # Prepare conversation for LLM
        messages = []
        
        # System message with instructions
        system_message = """
        You are an AI assistant that helps users find information in a memory system.
        Your task is to generate natural language responses based on search results.
        
        When generating responses:
        1. Summarize the search results in a clear, conversational manner
        2. Explain why certain memories were retrieved
        3. Provide specific details from the most relevant results
        4. If no results were found, suggest alternative search approaches
        5. Maintain a helpful, informative tone
        
        The search results will be provided in a structured format.
        """
        
        messages.append({"role": "system", "content": system_message})
        
        # Add conversation history
        if conversation_history:
            for message in conversation_history[-5:]:  # Include last 5 messages for context
                messages.append({"role": message["role"], "content": message["content"]})
        
        # Prepare search results for LLM
        results_text = json.dumps(search_results[:5], indent=2)  # Include only top 5 results
        
        # Add current query and results
        user_message = f"Query: {query}\n\nSearch Results: {results_text}"
        messages.append({"role": "user", "content": user_message})
        
        # Call LLM API
        if self.openai_api_key:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            result = response.choices[0].message.content
        elif self.anthropic_api_key:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=system_message,
                messages=[{"role": m["role"], "content": m["content"]} for m in messages if m["role"] != "system"]
            )
            result = response.content[0].text
        
        return result
    
    def _mock_generate_response(self, query, search_results):
        """Mock implementation for testing without API keys"""
        if not search_results:
            return f"I couldn't find any memories matching '{query}'. Would you like to try a different search term or approach?"
        
        num_results = len(search_results)
        response = f"I found {num_results} memories related to '{query}'."
        
        if num_results > 0:
            response += " Here's a summary of the most relevant information:\n\n"
            
            # Add details from top result
            top_result = search_results[0]
            content = top_result.get('content', 'No content available')
            content_preview = content[:100] + "..." if len(content) > 100 else content
            
            response += f"The most relevant memory mentions: '{content_preview}'\n\n"
            
            # Add tags if available
            if 'tags' in top_result and top_result['tags']:
                tags_text = ", ".join([f"{tag['value']} ({tag['type']})" for tag in top_result['tags'][:3]])
                response += f"This memory is tagged with: {tags_text}\n\n"
            
            # Suggest follow-up
            response += "Would you like more specific information about any of these memories?"
        
        return response
```

### 3. Integration Plan

#### 3.1 Update Flask App

```python
from flask import Flask, request, jsonify, render_template
from memory_search import MemorySearch
from query_understanding import QueryUnderstanding
from response_generation import ResponseGeneration
import os
import json

app = Flask(__name__)
memory_search = MemorySearch()

@app.route('/')
def index():
    return render_template('memory_search.html')

@app.route('/api/get-all-tags')
def get_all_tags():
    try:
        tags = memory_search.get_all_tags()
        return jsonify({
            'success': True,
            'tags': tags
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/search-memory', methods=['POST'])
def search_memory():
    try:
        data = request.json
        query = data.get('query', '')
        search_type = data.get('searchType', 'dual')
        tags = data.get('tags', [])
        limit = data.get('limit', 10)
        offset = data.get('offset', 0)
        
        if search_type == 'vector':
            results = memory_search.vector_search(query, limit=limit, offset=offset)
        elif search_type == 'tag':
            results = memory_search.tag_search(tags, limit=limit, offset=offset)
        else:
            results = memory_search.dual_search(query, tags=tags, limit=limit, offset=offset)
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),  # This would be replaced with actual total count
            'limit': limit,
            'search_type': search_type,
            'query': query
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/get-memory/<memory_id>')
def get_memory(memory_id):
    try:
        memory = memory_search.get_memory(memory_id)
        return jsonify({
            'success': True,
            'memory': memory
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        query = data.get('query', '')
        conversation_history = data.get('conversation_history', [])
        
        # Analyze query
        query_understanding = QueryUnderstanding()
        query_params = query_understanding.analyze_query(query, conversation_history)
        
        # Perform search based on extracted parameters
        search_results = []
        if query_params.get('search_type') == 'vector':
            search_results = memory_search.vector_search(query_params.get('query'))
        elif query_params.get('search_type') == 'tag':
            search_results = memory_search.tag_search(query_params.get('tags'))
        else:
            search_results = memory_search.dual_search(
                query_params.get('query'),
                tags=query_params.get('tags')
            )
        
        # Generate response
        response_generation = ResponseGeneration()
        response = response_generation.generate_response(
            query,
            search_results,
            conversation_history
        )
        
        return jsonify({
            'success': True,
            'response': response,
            'search_results': search_results,
            'search_type': query_params.get('search_type', 'dual'),
            'query': query_params.get('query', query),
            'total': len(search_results),
            'limit': 10
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Testing Plan

### 1. Unit Testing

- Test query understanding module with various query types
- Test response generation with different search results
- Test chat API endpoint with mock data

### 2. Integration Testing

- Test end-to-end flow from user input to response display
- Test interaction between conversational and structured search interfaces
- Test handling of edge cases (empty queries, no results, errors)

### 3. User Testing

- Test with real users to gather feedback on usability
- Test with real-world queries to evaluate response quality
- Test performance with large conversation histories

## Implementation Timeline

1. **Frontend Implementation (1-2 days)**
   - Add JavaScript functionality for chat interface
   - Implement message display and history management
   - Add typing indicators and error handling

2. **Backend Implementation (2-3 days)**
   - Create query understanding module
   - Implement response generation module
   - Add chat API endpoint

3. **Integration and Testing (1-2 days)**
   - Connect frontend and backend components
   - Test end-to-end functionality
   - Fix bugs and optimize performance

4. **Refinement and Documentation (1 day)**
   - Refine UI based on testing feedback
   - Optimize response generation
   - Document implementation details

## Conclusion

The conversational AI interface will provide a more intuitive and natural way for users to interact with the memory system. By combining the strengths of natural language understanding with the precision of structured search, the dual-mode interface will offer a comprehensive solution for memory retrieval.

The implementation plan outlined in this document provides a clear roadmap for completing the conversational interface, building on the existing memory search functionality and leveraging the power of modern LLMs for query understanding and response generation.
