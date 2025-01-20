import random


def replace_first_number(data, replaced=False):
    """
    Recursively iterate through a dictionary or list and replace the first encountered
    integer or float with a random number.

    Args:
        data: Input dictionary or list
        replaced: Flag to track if replacement has occurred

    Returns:
        Tuple of (modified data structure, boolean indicating if replacement occurred)
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if replaced:
                new_dict[key] = value
                continue

            if isinstance(value, str) and not replaced:
                if value.__contains__(".") and value.__contains__(".csv"):
                    new_dict[key] = random.randint(1, 100)
                    replaced = True
                    continue

            if isinstance(value, (int, float)) and not replaced:
                new_dict[key] = random.randint(1, 100)
                replaced = True
            elif isinstance(value, (dict, list)):
                new_value, replaced = replace_first_number(value, replaced)
                new_dict[key] = new_value
            else:
                new_dict[key] = value
        return new_dict, replaced

    elif isinstance(data, list):
        new_list = []
        for item in data:
            if replaced:
                new_list.append(item)
                continue

            if isinstance(item, (int, float)) and not replaced:
                new_list.append(random.randint(1, 100))
                replaced = True
            elif isinstance(item, (dict, list)):
                new_value, replaced = replace_first_number(item, replaced)
                new_list.append(new_value)
            else:
                new_list.append(item)
        return new_list, replaced

    return data, replaced
