# src/omega_agents/schemas.py

import re
import json
from typing import Any, Optional, Dict
from pydantic import BaseModel, ValidationError

# If you have them installed
from jsonschema import validate, ValidationError as JsonSchemaValidationError, Draft7Validator, SchemaError


class AgentOutputSchema(BaseModel):
    """
    Example of a structured output schema the user might define.
    This is just an example. You can create your own by subclassing BaseModel
    in your own code. Then pass that class to the supervisor as output_schema.
    """
    result: str
    confidence: float

def validate_json_structure(schema: Any) -> bool:
    """
    Check if the provided schema is valid JSON (list, dict, etc.).
    This function does NOT enforce JSON schema rules but ensures
    the input is a valid JSON structure.
    """
    try:
        # Ensure the schema is either a dictionary, list, or JSON-serializable
        if isinstance(schema, (dict, list)):
            return True
        else:
            raise ValueError("Output schema must be a dictionary or a list.")
    except ValueError as e:
        print(f"Invalid JSON structure: {e}")
        return False

def parse_type_from_description(description: str) -> str:
    """
    Extract the type name from the first parentheses in the description.
    E.g. '(str) The recommended activity.' -> 'string'
         '(int) The number of items.' -> 'integer'
    You can expand or customize this as needed for your domain.
    """
    # Use regex to find something inside the first parentheses
    match = re.match(r"\((.+?)\)", description.strip())
    if not match:
        # If no parentheses found, default to string or handle as you see fit
        return "string"

    raw_type = match.group(1).lower().strip()

    # Map raw_type to a JSON Schema type
    if raw_type in ["str", "string"]:
        return "string"
    elif raw_type in ["int", "integer"]:
        return "integer"
    elif raw_type in ["float", "double"]:
        return "float"
    elif raw_type in ["bool", "boolean"]:
        return "boolean"
    elif raw_type in ["null", "none"]:
        return "null"
    else:
        # Default or raise an error if you want strict handling
        return "string"

def validate_field(value: Any, expected_type: str, field_name: str):
    """
    Validate a single field based on the expected_type derived from the description.
    """
    if expected_type == "string":
        if not isinstance(value, str):
            raise ValueError(f"Field '{field_name}' should be a string but got {type(value).__name__}")
    elif expected_type == "integer":
        if not isinstance(value, int):
            raise ValueError(f"Field '{field_name}' should be an integer but got {type(value).__name__}")
    elif expected_type == "float":
        # In Python, float covers both float/double
        if not isinstance(value, float):
            raise ValueError(f"Field '{field_name}' should be a float but got {type(value).__name__}")
    elif expected_type == "boolean":
        if not isinstance(value, bool):
            raise ValueError(f"Field '{field_name}' should be a boolean but got {type(value).__name__}")
    elif expected_type == "null":
        if value is not None:
            raise ValueError(f"Field '{field_name}' should be null but got {type(value).__name__}")
    else:
        # You can add more specialized logic here if needed
        raise ValueError(f"Unsupported or unrecognized type '{expected_type}' for field '{field_name}'")

def validate_output_with_custom_schema(output_data: Any, schema: Dict[str, Any]) -> Optional[Any]:
    """
    Validate the output data against a custom schema format where type is derived from
    the description in properties.items.
    :param output_data: The agent's response (parsed JSON).
    :param schema: The custom schema with type embedded in the description.
    :return: The validated data if successful, or None if invalid.
    """
    try:
        # Infer type from schema properties if not explicitly provided
        expected_type = schema.get("type")
        if expected_type is None:
            if "properties" in schema:
                expected_type = "object"
            elif "items" in schema:
                expected_type = "array"
        
        if expected_type == "array":
            # Ensure output_data is a list
            if not isinstance(output_data, list):
                raise ValueError(f"Expected an array, but got {type(output_data).__name__}.")
            
            # Validate each item in the array
            item_schema = schema.get("items", {})
            for item in output_data:
                # We call our function recursively, because each item might be an object
                validate_output_with_custom_schema(item, item_schema)

        elif expected_type == "object":
            # Ensure output_data is a dictionary
            if not isinstance(output_data, dict):
                raise ValueError(f"Expected an object, but got {type(output_data).__name__}.")
            
            # Validate object properties
            properties = schema.get("properties", {})
            required_fields = schema.get("required", [])
            for field, description in properties.items():
                # Extract the expected type from the description
                expected_field_type = parse_type_from_description(description)
                if field in output_data:
                    # Validate the actual field
                    validate_field(output_data[field], expected_field_type, field)
                elif field in required_fields:
                    raise ValueError(f"Missing required field: {field}")

        elif expected_type == "string":
            # Ensure output_data is a string
            if not isinstance(output_data, str):
                raise ValueError(f"Expected a string, but got {type(output_data).__name__}.")

        elif expected_type == "integer":
            # Ensure output_data is an integer
            if not isinstance(output_data, int):
                raise ValueError(f"Expected an integer, but got {type(output_data).__name__}.")

        elif expected_type == "float":
            # Ensure output_data is a float
            if not isinstance(output_data, float):
                raise ValueError(f"Expected a float, but got {type(output_data).__name__}.")

        elif expected_type == "boolean":
            # Ensure output_data is a boolean
            if not isinstance(output_data, bool):
                raise ValueError(f"Expected a boolean, but got {type(output_data).__name__}.")

        elif expected_type == "null":
            # Ensure output_data is None
            if output_data is not None:
                raise ValueError(f"Expected null, but got {type(output_data).__name__}.")

        else:
            raise ValueError(f"Unsupported schema type: {expected_type}")

        # If no exceptions were raised, the data is valid
        return output_data

    except ValueError as e:
        print(f"Validation Error: {e}")
        return None