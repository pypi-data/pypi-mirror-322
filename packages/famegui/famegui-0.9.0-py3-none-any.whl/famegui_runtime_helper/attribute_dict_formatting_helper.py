from enum import Enum

from fameio.input.schema import AttributeType, AttributeSpecs


class StringAttributeType(Enum):
    BLOCK = "AttributeType.BLOCK"
    TIME_SERIES = "AttributeType.TIME_SERIES"
    ENUM = "AttributeType.ENUM"
    INTEGER = "AttributeType.INTEGER"
    LONG = "AttributeType.LONG"
    DOUBLE = "AttributeType.DOUBLE"
    STRING = "AttributeType.STRING"
    STRING_SET = "AttributeType.STRING_SET"


def get_full_attr_names(data, depth=None, current_depth=0):
    """
    Recursively extract full attribute names from nested data structure.

    Args:
        data: The nested data structure to process
        depth: Maximum depth to traverse (None for unlimited)
        current_depth: Current recursion depth

    Returns:
        list: Flat list of full attribute names
    """
    result = []

    # Return if we've reached max depth
    if depth is not None and current_depth >= depth:
        return result

    # Handle dictionary case
    if isinstance(data, dict):
        # Check if it's an attribute with 'attr' key
        if 'attr' in data:
            # Add the attribute name if it exists
            if isinstance(data['attr'], str):
                result.append(data['attr'])

            # Recursively process nested attributes
            if data.get('has_nested_attributes'):
                for key, value in data.get('attr', {}).items():
                    if isinstance(value, dict):
                        result.extend(get_full_attr_names(value, depth, current_depth + 1))

        # Process all dictionary values
        for value in data.values():
            if isinstance(value, (dict, list)):
                result.extend(get_full_attr_names(value, depth, current_depth + 1))

    # Handle list case
    elif isinstance(data, list):
        for item in data:
            result.extend(get_full_attr_names(item, depth, current_depth + 1))

    return result



def flatten_dict(full_dict: dict, d: dict, parent_key: str = '', sep: str = '.') -> dict:
    """
    Flatten a nested dictionary using dot notation, handling dictionaries and lists.

    Args:
        full_dict (dict): The original full dictionary for reference.
        d (dict or list): The current level dictionary or list to flatten.
        parent_key (str): The base key string accumulated so far.
        sep (str): The separator to use between keys.

    Returns:
        dict: A flattened dictionary with dot-separated keys.
    """
    items = {}
    end_node_keywords = ["mandatory", "list"]

    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k

            # Check for end node keywords to potentially skip or handle specially
            if any(keyword in k.lower() for keyword in end_node_keywords):
                # Depending on your specific needs, you can choose to skip or process differently
                pass  # Currently, we're processing all keys

            # Recursively process dictionaries and lists
            if isinstance(v, dict):
                items.update(flatten_dict(full_dict, v, new_key, sep))
            elif isinstance(v, list):
                items.update(flatten_dict(full_dict, v, new_key, sep))
            else:
                items[new_key] = v

    elif isinstance(d, list):
        new_key = parent_key

        items[new_key] = [sub_item for sub_item in d]

    return items



def get_nested_value(data, keys_list):
    for key in keys_list:
        if not isinstance(data, dict) and not isinstance(data, list):
            return data

        if isinstance(data, list):
            data = [sub_data[key] if key in sub_data else sub_data for sub_data in data]

            continue

        data = data[key] if key in data else data

    return data

def get_sub_attr(attr, flat_values, type_name):
    sub_dict = {}
    none_if_dict_or_list = lambda x: None if isinstance(x, dict) else x
    for key, item in attr:

        if not item.attr_type == AttributeType.BLOCK:
            item: AttributeSpecs

            value_key = item.full_name.replace(type_name + ".", "")
            alt_value = None

            if value_key.__contains__("."):
                keys = value_key.split(".")
                alt_value = get_nested_value(flat_values, keys)

                alt_value = alt_value if not isinstance(alt_value, dict) else None

            get_value_from_value_dict = lambda value_item_key: none_if_dict_or_list(
                flat_values[value_item_key]) if value_item_key in flat_values else None

            new_item = {
                "type": str(item.attr_type),
                "attr": item.full_name,
                "is_list": item.is_list,
                "flat_values": flat_values,
                "has_nested_attributes": item.has_nested_attributes,
                "is_mandatory": item.is_mandatory,
                "value": get_value_from_value_dict(value_key) if flat_values is not None else None,
                "value_key": value_key
            }

            if item.attr_type == AttributeType.ENUM:
                new_item["options"] = item.values

            if alt_value:
                new_item["value"] = none_if_dict_or_list(alt_value)

            sub_dict[key] = new_item

            continue
        value_key = item.full_name.replace(type_name + ".", "")

        alt_value = None

        get_value_from_value_dict = lambda value_item_key: none_if_dict_or_list(
            flat_values[value_item_key]) if value_item_key in flat_values else None

        new_item = {
            "type": str(item.attr_type),
            "attr_name": item.full_name,
            "attr": get_sub_attr(item.nested_attributes.items(), flat_values, type_name),
            "is_list": item.is_list,
            "alt_value": alt_value,
            "list_values": None,
            "is_mandatory": item.is_mandatory,
            "has_nested_attributes": item.has_nested_attributes,
            "flat_values": flat_values,
            "value": get_value_from_value_dict(value_key) if flat_values is not None else None,

        }
        if alt_value:
            new_item["value"] = alt_value if not isinstance(alt_value, dict) else None

        sub_dict[key] = new_item

    return sub_dict


def get_string_between_end_and_last_dot(input_string):
    if '.' in input_string:
        return input_string[input_string.rfind('.') + 1:]
    return


def build_simple_attr_dict(attr_spec: AttributeSpecs,
                           flat_full_name_labeled_values: dict,
                           agent_type_name: str, is_list_item=False):
    data_out = {}

    if attr_spec.has_nested_attributes:
        for key, item in attr_spec.nested_attributes.items():
            item: AttributeSpecs

            if item.has_nested_attributes:
                res_out = build_simple_attr_dict(item, flat_full_name_labeled_values,
                                                 agent_type_name,
                                                 is_list_item=item.is_list)

                data_out[key] = res_out
                continue

            full_name_without_agent_name = item.full_name.replace(agent_type_name + ".", "")

            data_out[key] = flat_full_name_labeled_values[
                full_name_without_agent_name] if full_name_without_agent_name in flat_full_name_labeled_values else None

        return data_out

    full_name_without_agent_name = attr_spec.full_name.replace(agent_type_name + ".", "")

    data_out[full_name_without_agent_name] = flat_full_name_labeled_values[
        full_name_without_agent_name] \
        if full_name_without_agent_name in flat_full_name_labeled_values else None

    return data_out
