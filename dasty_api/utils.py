import re
from time import time as get_current_time

def check_response_body_contains(json_data, yaml_data):
    """
    Checks if the specified items in the YAML content are found in the JSON data.

    Args:
        json_data: JSON data to be checked (can be a dict or a list).
        yaml_data: YAML content represented as a dictionary or a list.

    Returns:
        bool: True if all specified items are found in the JSON, False otherwise.
    """
    def check_item(json_item, yaml_item):
        if isinstance(yaml_item, dict):
            return isinstance(json_item, dict) and all(
                key in json_item and check_item(json_item[key], value) 
                for key, value in yaml_item.items()
            )
        if isinstance(yaml_item, list):
            return isinstance(json_item, list) and all(
                check_list_item(json_item, elem) for elem in yaml_item
            )
        return str(json_item) == str(yaml_item)

    def check_list_item(json_list, yaml_elem):
        if isinstance(yaml_elem, dict):
            return any(check_item(json_sub_item, yaml_elem) for json_sub_item in json_list)
        return yaml_elem in json_list

    if isinstance(yaml_data, list):
        return isinstance(json_data, list) and all(
            any(check_item(json_elem, yaml_elem) for json_elem in json_data) 
            for yaml_elem in yaml_data
        )

    if isinstance(yaml_data, dict):
        return all(check_item(json_data.get(key), value) for key, value in yaml_data.items())

    return str(json_data) == str(yaml_data)

def replace_variables_in_string(content: str, variables: dict) -> str:
    """
    Replaces variables in a string with their values from a dictionary.

    Args:
        content (str): String containing variables.
        variables (dict): Dictionary of variables and their values.

    Returns:
        str: String with variables replaced.
    """
    pattern = re.compile(r'\$\{(\w+)\}')
    return pattern.sub(lambda m: str(variables.get(m.group(1), m.group(0))), content)

def replace_variables(content, variables: dict):
    """
    Recursively replaces variables in content (supports dictionaries, lists, and strings).

    Args:
        content: Content with variables (dict, list, or str).
        variables (dict): Dictionary of variables and their values.

    Returns:
        Content with variables replaced.
    """
    if isinstance(content, dict):
        return {k: replace_variables(v, variables) for k, v in content.items()}
    if isinstance(content, list):
        return [replace_variables(item, variables) for item in content]
    if isinstance(content, str):
        return replace_variables_in_string(content, variables)
    return content

def check_response_length(json_data, response_length_spec):
    """
    Checks if the length of fields in JSON data matches specified lengths.

    Args:
        json_data: JSON data (dict, list, or string).
        response_length_spec: Expected lengths for fields or a single integer for overall length.

    Returns:
        bool: True if lengths match, False otherwise.
    """
    if isinstance(response_length_spec, int):
        assert len(json_data) == response_length_spec, \
            f"Length of response is {len(json_data)}, expected {response_length_spec}."
        return True

    if isinstance(response_length_spec, dict):
        for field, expected_length in response_length_spec.items():
            if field not in json_data:
                raise ValueError(f"Field '{field}' not found in the response.")
            assert len(json_data[field]) == expected_length, \
                f"Length of '{field}' is {len(json_data[field])}, expected {expected_length}."
        return True

    raise TypeError("response_length_spec must be an integer or a dictionary.")

def measure_time(func):
    """
    Measures the execution time of a function.

    Args:
        func: Function to measure.

    Returns:
        Tuple: Function response and execution time in milliseconds.
    """
    start_time = get_current_time()
    response = func()
    end_time = get_current_time()
    time_ms = f"{(end_time - start_time) * 1000:.2f}"
    return response, time_ms
