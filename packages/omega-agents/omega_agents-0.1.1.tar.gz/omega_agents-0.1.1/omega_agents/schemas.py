## src/omega_agents/schemas.py

"""
Pydantic schemas and optional output schema validation for structured responses.
"""

from pydantic import BaseModel, ValidationError
from typing import Any, Optional, Dict
from jsonschema import validate, ValidationError, Draft7Validator, SchemaError
import json

class AgentOutputSchema(BaseModel):
    """
    Example of a structured output schema the user might define.

    This is just an example. You can create your own by subclassing BaseModel
    in your own code. Then pass that class to the supervisor as output_schema.
    """
    result: str
    confidence: float

def validate_output_with_schema(output_data: Any, schema_model: BaseModel) -> Optional[Dict[str, Any]]:
    """
    Validate the output data against the provided Pydantic model.
    - If output_data is a string, attempt to parse it as JSON.
    - If output_data is already a dictionary, validate it directly.
    Return the validated dictionary if successful, or None if invalid.
    """
    try:
        # Parse string input to dictionary, if necessary
        if isinstance(output_data, str):
            output_data = json.loads(output_data)
        
        # Validate the dictionary against the schema
        validated = schema_model.parse_obj(output_data)
        return validated.dict()
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Validation Error: {e}")
        return None

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
    
def validate_json_schema(schema: Dict[str, Any]) -> bool:
    """
    Validates if the provided dictionary is a valid JSON schema.
    Returns True if the schema is valid, False otherwise.
    """
    try:
        Draft7Validator.check_schema(schema)
        return True
    except SchemaError as e:
        print(f"Invalid JSON schema: {e.message}")
        return False
    
def validate_output_with_json_schema(output_data: Any, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validate the output data against the provided JSON schema.
    Return the validated data if successful, or None if validation fails.
    """
    try:
        validate(instance=output_data, schema=schema)
        return output_data
    except ValidationError as e:
        print(f"Validation Error: {e.message}")
        return None