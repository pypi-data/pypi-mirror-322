import re


def process_key(s):
    result = s[s.rfind("."):] if s.__contains__(".") else s
    return result

def convert_to_int(s):
    # Extract the first sequence of digits from the string
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())  # Convert the matched digits to an integer
    else:
        raise ValueError("No valid integer found in the string")

def extract_id_from_contract_identifier(contract_identifier: str) -> int:
    index = contract_identifier.find('#')
    after_find = contract_identifier[index + 1:].strip() if index != -1 else None

    return convert_to_int(after_find)


def extract_product_name_from_contract_identifier(contract_identifier: str):
    parts = contract_identifier.split('(', 1)  # Split at first '('
    if len(parts) > 1:
        return parts[1].split(')', 1)[0]  # Extract the part before the first ')'
    return ""  # Return empty string if no parentheses are found


def get_last_substring(s):
    """
    Returns the substring after the last '.' in the input string.
    If no '.' is present, returns the original string.
    """
    return s.rsplit('.', 1)[-1]
