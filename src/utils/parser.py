import json
import re


def parse_json(input_string):
    # Remove leading and trailing whitespace
    input_string = input_string.strip()

    # Check if the input is in the 'json' block format
    if input_string.startswith('```json'):
        # Extract the JSON content between the backticks
        json_content = re.search(r'```json\s*(.*?)\s*```', input_string, re.DOTALL)
        if json_content:
            json_string = json_content.group(1)
        else:
            raise ValueError("Invalid JSON format")
    elif input_string.startswith('```'):
        # Extract the JSON content between the backticks
        json_content = re.search(r'```\s*(.*?)\s*```', input_string, re.DOTALL)
        if json_content:
            json_string = json_content.group(1)
        else:
            raise ValueError("Invalid JSON format")
    else:
        # Treat the input as normal JSON
        json_string = input_string

    # Attempt to parse the JSON
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON: {e}")