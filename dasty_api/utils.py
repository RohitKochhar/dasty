# Imports ---------------------------------------------------------------------
# Standard library imports
import json
import re

# Helper functions ------------------------------------------------------------- 
def check_response_body_contains(json_data, yaml_data):
    """
    Checks if the specified items in the YAML content are found in the JSON data.

    Parameters:
    json_data (dict): The JSON data to be checked.
    yaml_content (str): The YAML content as a string.

    Returns:
    bool: True if all specified items are found in the JSON, False otherwise.
    """
    def check_item(json_item, yaml_item):
        if isinstance(yaml_item, dict):
            return all(key in json_item and check_item(json_item[key], value) for key, value in yaml_item.items())
        elif isinstance(yaml_item, list):
            if all(isinstance(elem, dict) for elem in yaml_item):
                # For each dict in the yaml list, check if there's at least one matching dict in the json list
                return all(any(check_item(json_sub_item, yaml_sub_item) for json_sub_item in json_item) for yaml_sub_item in yaml_item)
            else:
                # If the list does not contain dicts, check if the yaml list is a subset of the json list
                return all(item in json_item for item in yaml_item)
        else:
            # For non-list, non-dict items, directly compare the values
            return str(json_item) == str(yaml_item)

    def traverse(json_data, yaml_data):
        for key, yaml_value in yaml_data.items():
            if key in json_data:
                if not check_item(json_data[key], yaml_value):
                    return False
            else:
                return False
        return True

    return traverse(json_data, yaml_data)

def replace_variables_in_string(content, variables):
    """
    Replaces all the variables specified with ${VARIABLE_NAME} in the content string
    with a value from the provided variables dictionary.
    """
    if not isinstance(content, str):
        content = str(content)  # Convert non-strings to strings
    pattern = re.compile(r'\$\{(\w+)\}')
    return pattern.sub(lambda m: str(variables.get(m.group(1), m.group(0))), content)

def replace_variables(content, variables):
    """
    Recursively replaces variables in a given content. The content can be a
    dictionary, list, or string. Variables are identified by the ${VARIABLE_NAME} syntax.
    """
    if isinstance(content, dict):
        return {k: replace_variables(v, variables) for k, v in content.items()}
    elif isinstance(content, list):
        return [replace_variables(item, variables) for item in content]
    elif isinstance(content, str):
        return replace_variables_in_string(content, variables)
    else:
        return content

def check_response_length(json_data, response_length_spec):
    for field, expected_length in response_length_spec.items():
        if field not in json_data:
            raise ValueError(f"Field '{field}' not found in the response.")

        actual_length = len(json_data[field])
        assert actual_length == expected_length, f"Length of '{field}' is {actual_length}, expected {expected_length}."
    return True
