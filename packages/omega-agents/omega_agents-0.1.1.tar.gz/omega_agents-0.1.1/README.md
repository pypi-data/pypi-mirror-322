# OmegaAgents

OmegaAgents is a scalable, production-ready multi-agent framework designed for complex task automation using a ReAct-like approach. It supports parallel agents, ephemeral memory, flexible tool registration, and structured output validation with JSON schemas.

---

## Features

- **Supervisor**: Manages multiple agents and orchestrates their workflows.
- **Ephemeral Memory**: Isolates agent memory to prevent unintended cross-talk.
- **Tools**: Register tools that agents can call at runtime, with flexible parameter handling.
- **JSON Schema Validation**: Enforce structured output using raw JSON schemas, supporting complex data types like arrays and nested objects.
- **Custom Goals and Behaviors**: Define agents with specific backgrounds, goals, and system prompts.
- **Logging Modes**: Verbose and debug modes for fine-grained monitoring.

---

## Installation

Install OmegaAgents directly from PyPI:

```bash
pip install omega-agents
```

---

## Usage

Below are examples demonstrating how to use OmegaAgents for various scenarios.

---

### **1. Without Tools and Without Output Schema**

This example shows a simple agent that produces free-text answers without using tools or output validation.

```python
from omega_agents.supervisor import Supervisor

def main():
    sup = Supervisor(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key",
        model_name="model",
        verbose=True,
        debug=False
    )

    # Create an agent
    agent_id = sup.create_agent(
        background="I am a general assistant",
        goal="Answer user questions to the best of my knowledge."
    )

    # Run the agent
    answer = sup.run_agent(agent_id, user_input="What is the capital of Japan?")
    print("\n[Final Agent Answer]")
    print(answer)

if __name__ == "__main__":
    main()
```

#### Expected Output:
```text
[Final Agent Answer]
The capital of Japan is Tokyo.
```

---

### **2. With Tools and Without Output Schema**

This example registers tools for the agent but does not enforce output validation.

```python
from omega_agents.supervisor import Supervisor
from omega_agents.tools import WeatherTool, ActivityTool

def main():
    sup = Supervisor(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key",
        model_name="model",
        verbose=True,
        debug=False
    )

    # Register default tools
    weather_tool = WeatherTool()
    activity_tool = ActivityTool()
    sup.register_tool(weather_tool)
    sup.register_tool(activity_tool)

    # Create an agent
    agent_id = sup.create_agent(
        background="I am an assistant that uses tools to provide accurate answers.",
        goal="Answer user queries using available tools."
    )

    # Run the agent
    answer = sup.run_agent(agent_id, user_input="What is the weather like in Tokyo today?")
    print("\n[Final Agent Answer]")
    print(answer)

if __name__ == "__main__":
    main()
```

#### Expected Output:
```text
[Final Agent Answer]
The weather in Tokyo today is sunny, with a temperature of 25°C.
```

---

### **3. Without Tools and With Output Schema**

In this example, the agent generates structured output based on a provided JSON schema.

```python
from omega_agents.supervisor import Supervisor

def main():
    sup = Supervisor(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key",
        model_name="model",
        verbose=True,
        debug=False
    )

    # Define a raw JSON schema
    output_schema = {
        "type": "object",
        "description": "A weather summary for a given location.",
        "properties": {
            "location": {"type": "string", "description": "The location being described."},
            "temperature": {"type": "string", "description": "The temperature at the location."},
            "condition": {"type": "string", "description": "The weather condition (e.g., sunny, rainy)."}
        },
        "required": ["location", "temperature", "condition"]
    }

    # Create an agent with an output schema
    agent_id = sup.create_agent(
        background="I am a weather reporting assistant",
        goal="Provide structured weather reports.",
        output_schema=output_schema
    )

    # Run the agent
    answer = sup.run_agent(agent_id, user_input="What is the weather in Tokyo?")
    print("\n[Final Agent Answer]")
    print(answer)

if __name__ == "__main__":
    main()
```

#### Expected Output:
```json
{
  "location": "Tokyo",
  "temperature": "25°C",
  "condition": "sunny"
}
```

---

### **4. With Tools and With Output Schema**

This example combines tools and structured output validation.

```python
from omega_agents.supervisor import Supervisor
from omega_agents.tools import WeatherTool, ActivityTool

def main():
    sup = Supervisor(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key",
        model_name="model",
        verbose=True,
        debug=False
    )

    # Register default tools
    weather_tool = WeatherTool()
    activity_tool = ActivityTool()
    sup.register_tool(weather_tool)
    sup.register_tool(activity_tool)

    # Define a raw JSON schema
    output_schema = {
        "type": "array",
        "description": "A list of recommended activities and their associated locations.",
        "items": {
            "type": "object",
            "description": "An activity recommendation for a specific location.",
            "properties": {
                "activity": {"type": "string", "description": "The recommended activity."},
                "location": {"type": "string", "description": "The location associated with the activity."}
            },
            "required": ["activity", "location"]
        }
    }

    # Create an agent with tools and output schema
    agent_id = sup.create_agent(
        background="I am a weather and activity recommendation assistant",
        goal="Suggest activities based on the current weather.",
        output_schema=output_schema
    )

    # Run the agent
    answer = sup.run_agent(agent_id, user_input="What should I do in Tokyo today?", output_schema=output_schema)
    print("\n[Final Agent Answer]")
    print(answer)

if __name__ == "__main__":
    main()
```

#### Expected Output:
```json
[
  {
    "activity": "Walk in the park",
    "location": "Tokyo"
  },
  {
    "activity": "Enjoy an outdoor cafe",
    "location": "Tokyo"
  }
]
```

---

## Advanced Features

- **Custom Tools**: Add your own tools by implementing the `ToolSchema` class.
- **Flexible Schemas**: Use JSON schemas to enforce output structure for better integration with downstream systems.
- **Ephemeral Memory**: Each agent’s memory is isolated and erased after the session.
- **Debugging Support**: Use verbose or debug modes to monitor agent interactions.

---

## How to Extend

1. **Define Custom Tools**:
   - Implement the `ToolSchema` interface and register it with the supervisor.
2. **Modify Prompts**:
   - Customize the agent’s behavior by providing specific backgrounds, goals, or system prompts.
3. **Dynamic Output Validation**:
   - Use JSON schemas to adapt to different output formats as needed.