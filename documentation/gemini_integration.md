# Gemini Flash 2.5 Integration

This document describes the integration of Google's Gemini Flash 2.5 model into the Kern Resources project.

## Overview

Gemini Flash 2.5 is Google's most affordable and efficient model, designed for processing large amounts of text quickly. It has a context window of up to 1 million tokens, making it ideal for tasks that require analyzing lengthy documents or large datasets.

Key features of Gemini Flash 2.5:
- Large context window (up to 1 million tokens)
- Cost-efficient processing
- Good performance on information extraction, summarization, and classification tasks
- Balanced capabilities for most general tasks

## Integration with Kern Resources

Gemini Flash 2.5 has been integrated into the Kern Resources project as a specialized model for data processing tasks. It complements the existing models (OpenAI, Anthropic, Groq) by providing a cost-efficient option for processing large amounts of text.

### Configuration

The Gemini Flash 2.5 model is configured in the following files:

1. **config.json**: The model is defined as the default for the "data_processor" role.
   ```json
   "models": {
       "default": "gpt-3.5-turbo",
       "researcher": "claude-3-sonnet",
       "analyst": "groq/meta-llama/llama-4-maverick-17b-128e-instruct",
       "documenter": "claude-3-sonnet",
       "integration": "gpt-3.5-turbo",
       "data_processor": "gemini-2.5-flash-preview-04-17"
   }
   ```

2. **llm_helper.py**: The model is defined as the default for the Google provider.
   ```python
   DEFAULT_MODELS = {
       "groq": "meta-llama/llama-4-maverick-17b-128e-instruct",
       "openai": "gpt-4o",
       "anthropic": "claude-3-5-sonnet-20241022",
       "google": "gemini-2.5-flash-preview-04-17"  # Use the full model name for Gemini Flash 2.5
   }
   ```

3. **.env file**: The Google API key is required for using Gemini models.
   ```
   # Google Gemini API Key (Required for Gemini models)
   # Format: Your Google API key from Google AI Studio or Google Cloud
   GOOGLE_API_KEY=your_api_key_here
   ```

## Integration Approaches

We've implemented two approaches for integrating Gemini Flash 2.5 into the Kern Resources project:

### Approach 1: Direct Integration with Google's SDK

This approach bypasses CrewAI and LiteLLM completely, using Google's Generative AI SDK directly. This is the most reliable approach and is recommended for most use cases.

```python
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key=your_api_key)

# Create a model instance
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

# Generate a response
response = model.generate_content("Your prompt here")

# Get the response text
print(response.text)
```

### Approach 2: Custom Adapter for CrewAI

We've created a custom adapter for CrewAI that uses Google's Generative AI SDK directly, bypassing LiteLLM. This approach is still experimental and may not work with all CrewAI features.

```python
from kern_resources.core.ai.gemini_adapter import create_data_processor_agent
from crewai import Task, Crew

# Create a data processor agent with Gemini adapter
agent = create_data_processor_agent()

# Create a task for the agent
task = Task(
    description="Your task description here",
    expected_output="Expected output description",
    agent=agent
)

# Create a crew with the agent and task
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

# Run the crew
result = crew.kickoff()
```

## Example Scripts

We've provided several example scripts to demonstrate the Gemini Flash 2.5 integration:

1. **test_gemini_direct.py**: A simple test script that uses Google's Generative AI SDK directly to test Gemini Flash 2.5.

2. **examples/gemini_flash_example.py**: A comprehensive example that demonstrates using Gemini Flash 2.5 for various data processing tasks, including extracting key points, summarizing, analyzing sentiment, and classifying text.

3. **test_gemini_adapter.py**: An experimental script that tries to use our custom Gemini adapter with CrewAI.

## Data Processing Capabilities

Gemini Flash 2.5 excels at the following data processing tasks:

### 1. Extracting Key Points

```python
from examples.gemini_flash_example import DataProcessor

processor = DataProcessor()
key_points = processor.extract_key_points(your_text)
```

### 2. Summarizing Text

```python
summary = processor.summarize(your_text, max_length=200)
```

### 3. Analyzing Sentiment

```python
sentiment = processor.analyze_sentiment(your_text)
```

### 4. Classifying Text

```python
classification = processor.classify(your_text, ["Technical", "Marketing", "Financial", "Educational"])
```

## Best Practices

- **Use Direct Integration**: For most use cases, use Google's Generative AI SDK directly rather than trying to integrate with CrewAI through LiteLLM.

- **Large Context Processing**: Use Gemini Flash 2.5 for tasks that involve processing large amounts of text, such as document analysis, summarization, and information extraction.

- **Cost Efficiency**: Gemini Flash 2.5 is more cost-efficient than models like GPT-4 or Claude 3.5 Sonnet, making it a good choice for tasks that don't require the highest level of reasoning capabilities.

- **Complementary Usage**: Use Gemini Flash 2.5 for data processing tasks and other models for tasks that require more complex reasoning or creative capabilities.

## Limitations

- Gemini Flash 2.5 is not as powerful as models like GPT-4 or Claude 3.5 Sonnet for complex reasoning tasks.
- It may not perform as well on creative writing or highly nuanced tasks.
- The model is optimized for efficiency rather than the highest quality outputs.
- Integration with CrewAI through LiteLLM is challenging due to compatibility issues with the newest Gemini models.

## Future Improvements

- Implement specialized tools for Gemini Flash 2.5 to leverage its large context window for document analysis.
- Create a vector search integration that uses Gemini Flash 2.5 for processing and embedding large documents.
- Develop a specialized agent role for document summarization using Gemini Flash 2.5.
- Improve the custom adapter for CrewAI to make it more reliable and compatible with all CrewAI features.
