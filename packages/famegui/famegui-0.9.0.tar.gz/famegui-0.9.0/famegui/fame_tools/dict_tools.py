def remove_none_values_and_empty_elements(item):
    """Recursively remove all None values and empty elements from a dictionary or list to clean up the data
    prepared for saving to a file
    """
    if isinstance(item, dict):
        # Handle dictionary: recursively clean its key-value pairs
        new_dict = {
            k: remove_none_values_and_empty_elements(v)
            for k, v in item.items()
            if v is not None
        }

        return {k: v for k, v in new_dict.items() if v not in [None, {}, []]}
    elif isinstance(item, list):
        # Handle list: recursively clean its elements
        new_list = [remove_none_values_and_empty_elements(v) for v in item]
        return [v for v in new_list if v not in [None, {}, []]]
    else:
        # Base case: return the item as-is
        return item