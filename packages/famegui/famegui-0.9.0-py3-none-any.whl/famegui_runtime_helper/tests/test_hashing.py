import pytest

from famegui_runtime_helper.dict_hash_helper import hash_dict


def test_hash_dict_consistency():
    """Test that hash_dict produces consistent hashes for identical dictionaries."""
    dict1 = {"key1": "value1", "key2": "value2"}
    dict2 = {"key2": "value2", "key1": "value1"}  # Same contents, different order

    hash1 = hash_dict(dict1)
    hash2 = hash_dict(dict2)

    assert hash1 == hash2, "Hashes should be the same for identical dictionaries"

def test_hash_dict_difference():
    """Test that hash_dict produces different hashes for different dictionaries."""
    dict1 = {"key1": "value1", "key2": "value2"}
    dict3 = {"key1": "value1", "key2": "different_value"}

    hash1 = hash_dict(dict1)
    hash3 = hash_dict(dict3)

    assert hash1 != hash3, "Hashes should be different for different dictionaries"

@pytest.mark.parametrize(
    "dict_input, expected_hash",
    [
        ({"key1": "value1", "key2": "value2"}, hash_dict({"key1": "value1", "key2": "value2"})),
        ({"a": 1, "b": [1, 2, 3]}, hash_dict({"a": 1, "b": [1, 2, 3]})),
        ({}, hash_dict({})),  # Empty dictionary
    ],
)

def test_hash_dict_with_parametrize(dict_input, expected_hash):
    """Test hash_dict with multiple cases using parametrize."""
    assert hash_dict(dict_input) == expected_hash, "Hash mismatch for input dictionary"