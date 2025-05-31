# Kern Resources Style Guide

This document defines the coding standards and style guidelines for the Kern Resources project.

## File Structure

Each Python file should follow this structure:

1. Module docstring (describing the purpose of the module)
2. Imports (grouped and ordered)
3. Constants
4. Classes and functions
5. Singleton instances (if applicable)

## Imports

Imports should be grouped and ordered as follows:

1. Standard library imports
2. Third-party library imports
3. Local application imports

Within each group, imports should be alphabetically ordered.

Example:
```python
# Standard library imports
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

# Third-party imports
import numpy as np
from crewai import Agent, Crew, Process

# Local application imports
from kern_resources.core.utils.config import config
from kern_resources.core.utils.env_manager import env_manager
```

## Docstrings

All modules, classes, and functions should have docstrings following the Google style:

```python
"""
Short description.

Longer description if needed.
"""

def function(arg1: type, arg2: type) -> return_type:
    """
    Short description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When and why this exception is raised
    """
```

## Type Hints

All function parameters and return values should have type hints.

```python
def function(arg1: str, arg2: Optional[int] = None) -> Dict[str, Any]:
    """Function documentation."""
    pass
```

## Error Handling

Error handling should be consistent across the codebase:

1. Use try/except blocks for operations that might fail
2. Log exceptions with appropriate level (error, warning, info)
3. Provide meaningful error messages
4. Re-raise exceptions when appropriate

Example:
```python
try:
    result = some_operation()
    return result
except SomeSpecificException as e:
    logger.error(f"Specific error occurred: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    import traceback
    logger.error(traceback.format_exc())
    return default_value
```

## Logging

Logging should be consistent across the codebase:

1. Use the module-level logger
2. Use appropriate log levels (debug, info, warning, error)
3. Provide meaningful log messages

Example:
```python
logger = logging.getLogger(__name__)

def function():
    logger.debug("Detailed information for debugging")
    logger.info("General information about operation")
    logger.warning("Warning about potential issues")
    logger.error("Error information when operation fails")
```

## Configuration Access

Access to configuration should be consistent:

1. Use the singleton config instance
2. Use the get method with a default value
3. Use dot notation for nested keys

Example:
```python
from kern_resources.core.utils.config import config

# Get configuration value with default
api_key = config.get("api_keys.openai", "default_key")
```

## Singleton Instances

Singleton instances should be created at the module level:

```python
# Create a singleton instance
config_manager = ConfigManager()
```

## Constants

Constants should be defined at the module level and use UPPER_CASE:

```python
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"
```

## Class and Function Names

1. Class names should use CamelCase
2. Function and method names should use snake_case
3. Private methods and attributes should start with an underscore

Example:
```python
class MyClass:
    def public_method(self):
        self._private_method()
    
    def _private_method(self):
        pass
```

## Line Length

Maximum line length should be 100 characters.

## Comments

1. Use comments sparingly and only when necessary
2. Comments should explain why, not what
3. TODO comments should include a description of what needs to be done

Example:
```python
# TODO: Implement vector search when Qdrant integration is complete
```

## Testing

1. All functions should have corresponding tests
2. Tests should be in a separate file with the same name as the module being tested
3. Test functions should start with `test_`

Example:
```python
# In test_config.py
def test_get_config_value():
    """Test getting a configuration value."""
    assert config.get("key", "default") == "expected_value"
```
