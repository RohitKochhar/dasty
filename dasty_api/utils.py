# Imports ---------------------------------------------------------------------
# Standard library imports
import json
import re

# Helper functions -----------------------------------------------------------
def replace_variables_in_string(content, variables):
    """
    Replaces all the variables specified with ${VARIABLE_NAME} in the content string
    with a value from the provided variables dictionary.
    
    Parameters:
        content (str): The content string
        variables (dict): The dictionary containing the variables and their values

    Returns:
        str: The content string with the variables replaced with their values

    Examples:
        >>> replace_variables_in_string('Hello ${name}', {'name': 'world'})
        'Hello world'
    """
    for var, value in variables.items():
        content = re.sub(rf'\$\{{{var}\}}', value, content)
    return content

def check_key_value_in_json(json_data, key, value):
    str = json.dumps(json_data)
    substr = f'"{key}": {value}'
    return substr in str

def replace_variables(content, variables):
    """
    Replaces all the variables specified with ${VARIABLE_NAME} in the content with
    a value from the provided variables dictionary.
    """
    if isinstance(content, dict):
        return {k: replace_variables(v, variables) for k, v in content.items()}
    elif isinstance(content, list):
        return [replace_variables(item, variables) for item in content]
    elif isinstance(content, str):
        return replace_variables_in_string(content, variables)
    else:
        return content

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
        elif isinstance(yaml_item, list) and all(isinstance(elem, dict) for elem in yaml_item):
            # Check if all dictionaries in yaml_item are matched in json_item
            return all(any(check_item(json_sub_item, yaml_sub_item) for json_sub_item in json_item) for yaml_sub_item in yaml_item)
        elif isinstance(yaml_item, list):
            return all(item in json_item for item in yaml_item)
        else:
            return json_item == yaml_item

    def traverse(json_data, yaml_data):
        for key, yaml_value in yaml_data.items():
            if key in json_data:
                if not check_item(json_data[key], yaml_value):
                    return False
            else:
                return False
        return True

    return traverse(json_data, yaml_data)
