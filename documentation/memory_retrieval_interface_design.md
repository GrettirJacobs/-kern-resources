# Memory Retrieval Interface Design

## Overview

The Memory Retrieval Interface is designed to provide a user-friendly way to search and retrieve information from the novel four-layer memory system. It combines vector-based semantic search with tag-based structured search to provide powerful and flexible retrieval capabilities.

## Design Principles

### 1. Dual Search Capabilities

The interface provides a unified search experience that intelligently combines vector-based semantic search with tag-based structured search:

- **Unified Search Bar**: A prominent search bar that intelligently determines whether to use vector or tag search based on the query
- **Advanced Search Options**: Expandable options for users who want to explicitly choose the search method
- **Confidence Scores**: Visual indicators of relevance for search results
- **Filtering Options**: Ability to filter by tags, dates, and other metadata

### 2. Layered Information Display

Following our four-layer memory architecture:

- **Layer 1 (Exact Content)**: Display the original, unmodified content
- **Layer 2 (Tags)**: Show relevant tags with visual indicators of their importance
- **Layer 3 (AI Summaries)**: Present concise AI-generated summaries of the content
- **Layer 4 (Meta-Commentaries)**: Highlight connections between related items

The interface allows users to toggle between these layers, providing different levels of abstraction and detail.

### 3. Conversational Interface

The interface incorporates a chat-like interaction model:

- **Natural Language Queries**: Allow users to ask questions about the stored resources
- **Query Refinement**: Enable users to refine search queries through conversation
- **Specific Requests**: Support requests for specific types of information
- **Explanations**: Provide explanations about why certain results were returned

### 4. Visual Knowledge Graph

The interface includes a visual representation of the memory system:

- **Connection Visualization**: Display connections between related resources
- **Interactive Exploration**: Allow users to explore through an interactive graph
- **Color Coding**: Use colors to indicate different sectors or categories
- **Zoom Levels**: Enable zooming in/out to adjust the level of detail

### 5. Contextual Awareness

The interface maintains context across interactions:

- **Session History**: Remember previous searches and their results
- **Reference Capability**: Allow users to reference previous results in new queries
- **Suggestions**: Provide suggestions based on search history
- **Persistent Sessions**: Support saving and resuming sessions

### 6. Adaptive Layout

The interface adapts to different devices, user preferences, and types of information:

- **Responsive Design**: Work well on different devices and screen sizes
- **User Preferences**: Adapt to user preferences and behavior
- **Multiple Views**: Provide different views (list, card, table, graph) for different types of information
- **Customization**: Allow users to customize the display based on their needs

## Implementation Plan

### Phase 1: Basic Search and Retrieval

1. **Search Page**:
   - Create a search page with a prominent search bar
   - Implement basic search functionality (vector, tag, dual)
   - Add simple filtering options

2. **Results Display**:
   - Display search results with basic information
   - Show relevance scores
   - Provide pagination

3. **Detail View**:
   - Create a detailed view for individual memory items
   - Display all layers of information
   - Show related memories

### Phase 2: Enhanced Visualization and Interaction

1. **Advanced Filtering**:
   - Add advanced filtering options
   - Implement sorting by different criteria
   - Add saved filters

2. **Layered Display**:
   - Implement toggles for different layers
   - Add collapsible sections
   - Provide context-sensitive help

3. **Basic Visualization**:
   - Create a simple graph view of connections
   - Implement basic interaction with the graph
   - Add visual indicators of relationship strength

4. **Conversational Elements**:
   - Add suggested queries
   - Implement query refinement
   - Add explanations for search results

### Phase 3: Advanced Features

1. **Full Conversational Interface**:
   - Implement a chat-like interface
   - Add natural language understanding
   - Support complex queries and follow-up questions

2. **Interactive Knowledge Graph**:
   - Create a fully interactive graph view
   - Add filtering and highlighting in the graph
   - Implement path finding between memories

3. **Contextual Features**:
   - Add session history
   - Implement context-aware suggestions
   - Support saving and sharing searches

4. **Customization**:
   - Add user preferences
   - Implement custom views
   - Support themes and layouts

## UI Components

### Search Interface

```
+-----------------------------------------------------------------------+
|                                                                       |
|  [ Search memories...                                       ] [Search] |
|                                                                       |
|  [ ] Advanced Search Options                                          |
|      Search Type: [Vector ▼]  Tags: [Add Tags +]  Limit: [10 ▼]       |
|                                                                       |
+-----------------------------------------------------------------------+
```

### Results Display

```
+-----------------------------------------------------------------------+
| Found 42 results for "healthcare resources in Bakersfield"            |
|                                                                       |
| Filters: [Sector: Healthcare ×] [City: Bakersfield ×] [Clear All]     |
|                                                                       |
| Sort by: [Relevance ▼]                                                |
|                                                                       |
| +-------------------------------------------------------------------+ |
| | Bakersfield Memorial Hospital                                     | |
| | Sector: Healthcare  |  City: Bakersfield  |  Relevance: 95%       | |
| |                                                                   | |
| | Provides emergency services, specialized care, and community      | |
| | health programs. Located at 420 34th Street.                      | |
| |                                                                   | |
| | [View Details]                                [Save] [Share]      | |
| +-------------------------------------------------------------------+ |
|                                                                       |
| +-------------------------------------------------------------------+ |
| | Kern Medical Center                                               | |
| | Sector: Healthcare  |  City: Bakersfield  |  Relevance: 92%       | |
| |                                                                   | |
| | County hospital providing comprehensive medical services,         | |
| | including emergency care, specialty clinics, and training.        | |
| |                                                                   | |
| | [View Details]                                [Save] [Share]      | |
| +-------------------------------------------------------------------+ |
|                                                                       |
| [1] [2] [3] [4] [5] ... [Next >]                                      |
+-----------------------------------------------------------------------+
```

### Detail View

```
+-----------------------------------------------------------------------+
| < Back to Results                                                      |
|                                                                        |
| # Bakersfield Memorial Hospital                                        |
| Sector: Healthcare  |  City: Bakersfield  |  Verified: 2025-03-15     |
|                                                                        |
| ## Contact Information                                                 |
| Phone: (661) 327-1792                                                  |
| Address: 420 34th Street, Bakersfield, CA 93301                        |
| Website: https://www.dignityhealth.org/central-california/locations/   |
|          memorial-hospital                                             |
|                                                                        |
| ## Services                                                            |
| - Emergency Services                                                   |
| - Specialized Care                                                     |
| - Community Health Programs                                            |
|                                                                        |
| ## Eligibility                                                         |
| Open to all patients. Insurance accepted. Financial assistance         |
| available for qualifying individuals.                                  |
|                                                                        |
| ## Hours                                                               |
| Emergency: 24/7                                                        |
| General: Monday-Friday 8:00 AM - 5:00 PM                               |
|                                                                        |
| ## AI Analysis                                                         |
| [Toggle ▼]                                                             |
| Bakersfield Memorial Hospital is a comprehensive healthcare facility   |
| serving the Bakersfield community with a wide range of services.       |
| The hospital is particularly notable for its emergency services and    |
| specialized care programs. It accepts most insurance plans and offers  |
| financial assistance, making it accessible to a broad population.      |
|                                                                        |
| ## Related Resources                                                   |
| [Graph View] [List View]                                               |
|                                                                        |
| - Kern Medical Center (92% related)                                    |
| - Bakersfield Family Medical Center (85% related)                      |
| - Omni Family Health (78% related)                                     |
|                                                                        |
+-----------------------------------------------------------------------+
```

### Knowledge Graph View

```
+-----------------------------------------------------------------------+
|                                                                       |
|    [Zoom +] [Zoom -] [Reset] [Filters ▼] [Legend ▼]                   |
|                                                                       |
|    +-------+                                                          |
|    |       |                                                          |
|    | BMH   |                                                          |
|    |       |                                                          |
|    +-------+                                                          |
|        |                                                              |
|        |                                                              |
|    +-------+     +-------+     +-------+                              |
|    |       |     |       |     |       |                              |
|    | KMC   |-----| BFMC  |-----| OFH   |                              |
|    |       |     |       |     |       |                              |
|    +-------+     +-------+     +-------+                              |
|        |             |             |                                  |
|        |             |             |                                  |
|    +-------+     +-------+     +-------+                              |
|    |       |     |       |     |       |                              |
|    | ADPH  |     | CBCC  |     | KCDPH |                              |
|    |       |     |       |     |       |                              |
|    +-------+     +-------+     +-------+                              |
|                                                                       |
|    Legend:                                                            |
|    ● Healthcare Facilities  ● Public Health  ● Community Services     |
|                                                                       |
+-----------------------------------------------------------------------+
```

## API Design

### Search Memories

**Endpoint**: `/api/search-memory`

**Method**: POST

**Request Body**:
```json
{
  "query": "healthcare resources in Bakersfield",
  "searchType": "dual",
  "tags": [
    { "type": "city", "value": "Bakersfield" },
    { "type": "sector", "value": "Healthcare" }
  ],
  "limit": 10,
  "offset": 0
}
```

**Response**:
```json
{
  "success": true,
  "search_type": "dual",
  "query": "healthcare resources in Bakersfield",
  "tags": [
    { "type": "city", "value": "Bakersfield" },
    { "type": "sector", "value": "Healthcare" }
  ],
  "results": [
    {
      "memory_id": "abc123",
      "content": "...",
      "metadata": { ... },
      "tags": [ ... ],
      "ai_analysis": { ... },
      "vector_score": 0.95,
      "tag_score": 1.0,
      "combined_score": 0.975
    },
    ...
  ],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

### Get Memory

**Endpoint**: `/api/get-memory/<memory_id>`

**Method**: GET

**Response**:
```json
{
  "success": true,
  "memory": {
    "memory_id": "abc123",
    "content": "...",
    "metadata": { ... },
    "tags": [ ... ],
    "ai_analysis": { ... },
    "meta_analyses": [ ... ]
  }
}
```

### Get All Tags

**Endpoint**: `/api/get-all-tags`

**Method**: GET

**Response**:
```json
{
  "success": true,
  "tags": {
    "sector": ["Healthcare", "Education", "Housing", ...],
    "city": ["Bakersfield", "Taft", "Delano", ...],
    "service": ["Emergency", "Counseling", "Training", ...],
    ...
  }
}
```

## Conclusion

The Memory Retrieval Interface is designed to provide a powerful and intuitive way to search and retrieve information from the novel memory system. By combining vector-based semantic search with tag-based structured search, and presenting information in layers from raw content to AI-generated insights, the interface enables users to find and understand the information they need quickly and effectively.

The phased implementation approach allows for incremental development and testing, with each phase building on the previous one to add more advanced features and capabilities.
