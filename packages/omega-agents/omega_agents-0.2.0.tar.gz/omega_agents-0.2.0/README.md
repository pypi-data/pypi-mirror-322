# OmegaAgents

OmegaAgents is a scalable, production-ready multi-agent framework designed for complex task automation using a ReAct-like approach. It supports parallel agents, ephemeral memory, flexible tool registration, and structured output validation with JSON schemas.

[![PyPI version](https://badge.fury.io/py/omega-agents.svg)](https://badge.fury.io/py/omega-agents)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Basic Agent](#1-basic-agent-without-tools-and-without-output-schema)
  - [Using Tools](#2-using-tools-without-output-schema)
  - [Structured Output](#3-using-output-schema-without-tools)
  - [Advanced Usage](#4-combining-tools-and-structured-output)
- [Creating Custom Tools](#creating-custom-tools)
  - [Tool Components](#tool-components)
  - [Complete Custom Tool Example](#complete-custom-tool-example)
- [Output Schema Validation](#output-schema-validation)
- [Advanced Features](#advanced-features)
- [Best Practices](#best-practices)
- [Contributing](#contributing)
- [License](#license)

## Features

- **🎯 Supervisor**: Manages multiple agents and orchestrates their workflows
- **🧠 Ephemeral Memory**: Isolates agent memory to prevent unintended cross-talk
- **🛠️ Tools**: Register tools that agents can call at runtime, with flexible parameter handling
- **📋 JSON Schema Validation**: Enforce structured output using raw JSON schemas
- **🎭 Custom Goals and Behaviors**: Define agents with specific backgrounds, goals, and system prompts
- **📝 Logging Modes**: Verbose and debug modes for fine-grained monitoring

## Installation

Install OmegaAgents directly from PyPI:

```bash
!pip install omega_agents --extra-index-url https://pypi.fury.io/omega/

# Username: 
# Password: 
```

## Quick Start

```python
from omega_agents.supervisor import Supervisor

# Initialize the supervisor
sup = Supervisor(
    base_url="https://api.openai.com/v1",
    api_key="your-api-key",
    model_name="model",
    verbose=True
)

# Create an agent
agent_id = sup.create_agent(
    background="I am a general assistant",
    goal="Answer user questions helpfully."
)

# Run the agent
answer = sup.run_agent(agent_id, user_input="What is OmegaAgents?")
print(answer)
```

## Usage Examples

### 1. Basic Agent (Without Tools and Without Output Schema)

This example shows a simple agent that produces free-text answers:

```python
from omega_agents.supervisor import Supervisor

def main():
    sup = Supervisor(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key",
        model_name="model"
    )

    agent_id = sup.create_agent(
        background="I am a general assistant",
        goal="Answer user questions to the best of my knowledge."
    )

    answer = sup.run_agent(
        agent_id, 
        user_input="What is the capital of Japan?"
    )
    print(answer)

if __name__ == "__main__":
    main()
```

### 2. Using Tools (Without Output Schema)

Example showing how to use built-in tools:

```python
from omega_agents.supervisor import Supervisor
from omega_agents.tools import WeatherTool, ActivityTool

def main():
    sup = Supervisor(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key"
    )

    # Register tools
    sup.register_tool(WeatherTool())
    sup.register_tool(ActivityTool())

    agent_id = sup.create_agent(
        background="I am a weather and activity assistant",
        goal="Help users with weather-based activity planning."
    )

    answer = sup.run_agent(
        agent_id,
        user_input="What should I do in Tokyo today?"
    )
    print(answer)
```

### 3. Using Output Schema (Without Tools)

Example demonstrating structured output validation:

```python
from omega_agents.supervisor import Supervisor

def main():
    sup = Supervisor(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key"
    )

    # Define output schema
    output_schema = {
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "temperature": {"type": "string"},
            "condition": {"type": "string"}
        },
        "required": ["location", "temperature", "condition"]
    }

    agent_id = sup.create_agent(
        background="I am a weather reporting assistant",
        goal="Provide structured weather reports.",
        output_schema=output_schema
    )

    answer = sup.run_agent(
        agent_id,
        user_input="What's the weather in Tokyo?",
        output_schema=output_schema
    )
    print(answer)
```

### 4. Combining Tools and Structured Output

Advanced example using both tools and output validation:

```python
from omega_agents.supervisor import Supervisor
from omega_agents.tools import WeatherTool, ActivityTool

def main():
    sup = Supervisor(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key"
    )

    # Register tools
    sup.register_tool(WeatherTool())
    sup.register_tool(ActivityTool())

    # Define output schema
    output_schema = {
        "type": "array",
        "items": {
            "properties": {
                "activity": {"type": "string"},
                "location": {"type": "string"}
            },
            "required": ["activity", "location"]
        }
    }

    agent_id = sup.create_agent(
        background="I recommend activities based on weather",
        goal="Suggest weather-appropriate activities",
        output_schema=output_schema
    )

    answer = sup.run_agent(
        agent_id,
        user_input="What should I do in Tokyo today?",
        output_schema=output_schema
    )
    print(answer)
```

## Creating Custom Tools

### Tool Components

Every custom tool requires:

1. A `ToolSchema` defining metadata and parameters
2. An `execute()` method implementing the functionality

### Basic Template

```python
from omega_agents.tools import ToolSchema
from typing import List, Dict, Any

class MyCustomTool:
    def __init__(self):
        self.schema = ToolSchema(
            name="my_tool",
            description="Tool description",
            parameters={
                "param1": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            required=["param1"],
            tool=self
        )

    def execute(
        self,
        conversation: List[Dict[str, str]],
        context: Dict[str, Any],
        **params
    ) -> Dict[str, Any]:
        # Tool logic here
        return {"result": "value"}
```

### Complete Custom Tool Example

Here's a complete example that demonstrates creating and using custom tools for a movie recommendation system:

```python
# custom_tools.py
from omega_agents.tools import ToolSchema
from typing import List, Dict, Any
import requests

class MovieDatabaseTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.schema = ToolSchema(
            name="movie_search",
            description="Search for movies and get recommendations",
            parameters={
                "query": {
                    "type": "string",
                    "description": "Movie title or search term"
                },
                "year": {
                    "type": "integer",
                    "description": "Release year (optional)"
                },
                "genre": {
                    "type": "string",
                    "description": "Movie genre (optional)"
                }
            },
            required=["query"],
            tool=self
        )

    def execute(
        self,
        conversation: List[Dict[str, str]],
        context: Dict[str, Any],
        **params
    ) -> Dict[str, Any]:
        query = params["query"]
        year = params.get("year")
        genre = params.get("genre")
        
        # Simulated API call
        movies = [
            {"title": f"Movie about {query}", "year": year or 2024, "genre": genre or "Drama"},
            {"title": f"Another {query} film", "year": year or 2023, "genre": genre or "Action"}
        ]
        
        return {
            "search_results": movies,
            "total_results": len(movies)
        }

class MovieReviewTool:
    def __init__(self):
        self.schema = ToolSchema(
            name="movie_review",
            description="Get movie reviews and ratings",
            parameters={
                "movie_id": {
                    "type": "string",
                    "description": "Movie ID to get reviews for"
                }
            },
            required=["movie_id"],
            tool=self
        )

    def execute(
        self,
        conversation: List[Dict[str, str]],
        context: Dict[str, Any],
        **params
    ) -> Dict[str, Any]:
        movie_id = params["movie_id"]
        
        # Simulated reviews
        reviews = [
            {"rating": 4.5, "text": "Great movie!", "author": "Reviewer1"},
            {"rating": 4.0, "text": "Highly recommended", "author": "Reviewer2"}
        ]
        
        return {
            "movie_id": movie_id,
            "average_rating": sum(r["rating"] for r in reviews) / len(reviews),
            "reviews": reviews
        }

# main.py
from omega_agents.supervisor import Supervisor
from custom_tools import MovieDatabaseTool, MovieReviewTool

def main():
    # Initialize supervisor
    sup = Supervisor(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key",
        model_name="model",
        verbose=True
    )

    # Create and register custom tools
    movie_db = MovieDatabaseTool(api_key="movie-db-api-key")
    movie_review = MovieReviewTool()
    sup.register_tool(movie_db)
    sup.register_tool(movie_review)

    # Define output schema for movie recommendations
    output_schema = {
        "type": "array",
        "items": {
            "properties": {
                "title": {"type": "string", "description": "Movie title"},
                "rating": {"type": "number", "description": "Average rating"},
                "recommendation_reason": {"type": "string", "description": "Why this movie is recommended"}
            },
            "required": ["title", "rating", "recommendation_reason"]
        }
    }

    # Create movie recommendation agent
    agent_id = sup.create_agent(
        background="I am a movie recommendation expert",
        goal="Recommend movies based on user preferences and provide ratings",
        output_schema=output_schema,
        additional_instructions=[
            "Use both movie search and review tools to make informed recommendations",
            "Consider both movie metadata and user reviews in recommendations",
            "Provide specific reasons for each recommendation"
        ]
    )

    # Run the agent
    user_query = "Can you recommend some drama movies about friendship?"
    answer = sup.run_agent(agent_id, user_input=user_query, output_schema=output_schema)
    print("\nMovie Recommendations:")
    print(answer)

if __name__ == "__main__":
    main()
```

Expected output:
```json
Movie Recommendations:
[
  {
    "title": "Movie about friendship",
    "rating": 4.25,
    "recommendation_reason": "Strong drama about friendship with excellent reviews"
  },
  {
    "title": "Another friendship film",
    "rating": 4.0,
    "recommendation_reason": "Compelling story and high user ratings"
  }
]
```

## Output Schema Validation

OmegaAgents supports JSON Schema validation for structured outputs:

### Basic Schema Types

```python
# Object Schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name"]
}

# Array Schema
schema = {
    "type": "array",
    "items": {
        "properties": {
            "field1": {"type": "string"},
            "field2": {"type": "number"}
        }
    }
}
```

### Advanced Schema Features

- Nested objects
- Array validation
- Required fields
- Type validation
- Custom descriptions

## Advanced Features

### 1. Ephemeral Memory
- Each agent maintains isolated memory
- Memory is cleared after session completion
- Prevents cross-contamination between agents

### 2. Debugging Support
```python
sup = Supervisor(
    base_url="your-url",
    api_key="your-key",
    verbose=True,  # Enable normal logging
    debug=True     # Enable detailed debugging
)
```

### 3. Custom Instructions
```python
agent_id = sup.create_agent(
    background="Agent background",
    goal="Agent goal",
    additional_instructions=[
        "Follow specific guideline 1",
        "Follow specific guideline 2"
    ]
)
```

## Best Practices

### Tool Development
- Use clear, descriptive names
- Provide detailed parameter descriptions
- Handle optional parameters gracefully
- Implement comprehensive error handling
- Return well-structured data

### Schema Design
- Define clear property types
- Include meaningful descriptions
- List all required fields
- Use appropriate validation rules

### Agent Configuration
- Set focused backgrounds
- Define clear goals
- Provide specific instructions
- Use appropriate logging levels

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.