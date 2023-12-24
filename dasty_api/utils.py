import re

def check_response_body_contains(json_data: dict, yaml_data: dict) -> bool:
    """
    Checks if the specified items in the YAML content are found in the JSON data.

    Args:
        json_data (dict): The JSON data to be checked.
        yaml_data (dict): The YAML content represented as a dictionary.

    Returns:
        bool: True if all specified items are found in the JSON, False otherwise.
    """
    def check_item(json_item, yaml_item):
        if isinstance(yaml_item, dict):
            return all(key in json_item and check_item(json_item[key], value) 
                       for key, value in yaml_item.items())
        if isinstance(yaml_item, list):
            # For each element in the yaml list, check if it's matched in the json list
            return all(check_list_item(json_item, elem) for elem in yaml_item)
        return str(json_item) == str(yaml_item)

    def check_list_item(json_list, yaml_elem):
        if isinstance(yaml_elem, dict):
            return any(check_item(json_sub_item, yaml_elem) for json_sub_item in json_list)
        return yaml_elem in json_list

    return all(check_item(json_data.get(key), value) for key, value in yaml_data.items())

def replace_variables_in_string(content: str, variables: dict) -> str:
    """
    Replaces all the variables in the content string with their values from the variables dictionary.

    Args:
        content (str): The string content with variables.
        variables (dict): Dictionary of variables to replace in the content.

    Returns:
        str: Content string with variables replaced.
    """
    pattern = re.compile(r'\$\{(\w+)\}')
    return pattern.sub(lambda m: str(variables.get(m.group(1), m.group(0))), content)

def replace_variables(content, variables: dict):
    """
    Recursively replaces variables in content. Supports dictionaries, lists, and strings.

    Args:
        content: The content (dict, list, or str) with variables.
        variables (dict): Dictionary of variables to replace in the content.

    Returns:
        The content with variables replaced.
    """
    if isinstance(content, dict):
        return {k: replace_variables(v, variables) for k, v in content.items()}
    if isinstance(content, list):
        return [replace_variables(item, variables) for item in content]
    if isinstance(content, str):
        return replace_variables_in_string(content, variables)
    return content

def check_response_length(json_data: dict, response_length_spec: dict) -> bool:
    """
    Checks if the length of fields in JSON data matches the specified lengths.

    Args:
        json_data (dict): The JSON data to be checked.
        response_length_spec (dict): Specification of expected lengths for fields.

    Returns:
        bool: True if all fields match their specified lengths, False otherwise.
    """
    for field, expected_length in response_length_spec.items():
        if field not in json_data:
            raise ValueError(f"Field '{field}' not found in the response.")
        actual_length = len(json_data[field])
        assert actual_length == expected_length, \
            f"Length of '{field}' is {actual_length}, expected {expected_length}."
    return True
