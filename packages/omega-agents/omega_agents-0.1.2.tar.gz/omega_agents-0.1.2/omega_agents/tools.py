## src/omega_agents/tools.py

"""
Define your default or user-provided tools here.
Users can add their own as well.
"""

from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ToolSchema:
    """
    Metadata for a tool: name, description, parameters, required fields,
    plus a reference to the tool's execute() function.
    """
    name: str
    description: str
    parameters: Dict[str, Any]
    required: List[str]
    tool: Any  # The actual Python object with an 'execute()' method.

class WeatherTool:
    """
    Example weather tool returning fake data.
    """
    def __init__(self):
        self.schema = ToolSchema(
            name="weather",
            description="Get current weather data for a location",
            parameters={
                "location": {
                    "type": "string",
                    "description": "City name or coordinates"
                },
                "units": {
                    "type": "string",
                    "description": "Units for temperature (celsius/fahrenheit)"
                }
            },
            required=["location"],
            tool=self
        )

    def execute(
        self,
        conversation: List[Dict[str, str]],
        context: Dict[str, Any],
        **params
    ) -> Dict[str, Any]:
        location = params.get("location", "New York")
        units = params.get("units", "celsius")
        temperature_c = 25
        temperature_f = (temperature_c * 9/5) + 32

        return {
            "location": location,
            "units": units,
            "temperature": temperature_c if units == "celsius" else temperature_f,
            "condition": "sunny",
            "humidity": 60,
            "wind_speed": 10
        }

class ActivityTool:
    """
    Example activity tool that recommends things to do based on weather.
    """
    def __init__(self):
        self.schema = ToolSchema(
            name="activity",
            description="Recommend activities based on weather conditions",
            parameters={
                "temperature": {
                    "type": "number",
                    "description": "Current temperature"
                },
                "condition": {
                    "type": "string",
                    "description": "Weather condition (e.g. sunny/rainy)"
                },
                "wind_speed": {
                    "type": "number",
                    "description": "Wind speed in km/h"
                }
            },
            required=["temperature", "condition"],
            tool=self
        )

    def execute(
        self,
        conversation: List[Dict[str, str]],
        context: Dict[str, Any],
        **params
    ) -> Dict[str, Any]:
        temperature = params.get("temperature")
        condition = params.get("condition")
        wind_speed = params.get("wind_speed", 0)

        recommended = {
            "outdoor": [],
            "indoor": ["Visit museums", "Shopping", "Indoor sports"]
        }

        if condition.lower() == "sunny" and 15 <= temperature <= 30 and wind_speed < 20:
            recommended["outdoor"].extend([
                "Walk in the park",
                "Enjoy an outdoor cafe",
                "Go sightseeing"
            ])
        if 20 <= temperature <= 28 and wind_speed < 15:
            recommended["outdoor"].append("Beach day")

        return {
            "weather_summary": {
                "temperature": temperature,
                "condition": condition,
                "wind_speed": wind_speed
            },
            "recommendations": recommended
        }