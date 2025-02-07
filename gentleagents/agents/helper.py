from typing import Callable, Dict, Any, get_type_hints
import inspect

GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"
BOX_LINE = "-" * 110


def format_final_response(response: str) -> str:
    """Formats the final response to make it stand out in the terminal."""
    return f"\n{GREEN}{BOX_LINE}\n{BOLD}{response}{RESET}\n{GREEN}{BOX_LINE}{RESET}\n"


def python_type_to_json_schema(py_type: type) -> Dict[str, Any]:
    """Convert a Python type to a JSON Schema snippet."""
    try:
        mapping = {
            int: {"type": "integer"},
            float: {"type": "number"},
            str: {"type": "string"},
            bool: {"type": "boolean"},
        }

        if py_type in mapping:
            return mapping[py_type]

        print(f"Warning: Unsupported type '{py_type}'. Defaulting to 'string'.")
        return {"type": "string"}

    except Exception as e:
        print(f"Error converting Python type '{py_type}' to JSON Schema: {e}")
        return {"type": "string"}

def get_function_parameters(func: Callable) -> Dict[str, Any]:
    """
    Extracts parameters from a function and returns a JSON Schema.

    Returns a schema like:
    {
        "type": "object",
        "properties": {
            "a": {"type": "integer"},
            "b": {"type": "integer"}
        },
        "required": ["a", "b"]
    }
    """
    try:
        signature = inspect.signature(func)
        properties = {}
        required = []

        for name, param in signature.parameters.items():
            try:
                if param.annotation is inspect._empty:
                    json_type = {"type": "string"}
                else:
                    json_type = python_type_to_json_schema(param.annotation)

                properties[name] = json_type

                if param.default is inspect._empty:
                    required.append(name)

            except Exception as e:
                print(f"Error processing parameter '{name}' in function '{func.__name__}': {e}")
                properties[name] = {"type": "string"}  

        schema = {"type": "object", "properties": properties}

        if required:
            schema["required"] = required

        return schema

    except Exception as e:
        print(f"Error extracting function signature for '{func}': {e}")
        return {"type": "object", "properties": {}} 