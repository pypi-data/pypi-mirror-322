import json
import timeit
from typing import Dict, Any, Tuple, Optional


class DictDiffer:
    """
        A utility class for comparing two dictionaries and identifying differences.
    """

    @staticmethod
    def diff_direct(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> dict[str, dict[str, Optional[Any]]]:
        """
        Compares two dictionaries and identifies differences in their keys and values.

        This method uses sets to efficiently find differences and a dictionary comprehension
        to build the result.

        Args:
             dict1 (Dict[str, Any]): The first dictionary to compare.
             dict2 (Dict[str, Any]): The second dictionary to compare.

        Returns:
                Dict[str, Dict[str, Any]]: A dictionary containing the keys that are different
                                            between `dict1` and `dict2`, along with their respective
                                            old and new values.
                                            - If a key is missing in one of the dictionaries,
                                            the corresponding value will be `None`.
                                            Example:
                                                {
                                                    "key1": {"old_value": 1, "new_value": 2},
                                                    "key2": {"old_value": None, "new_value": 3}
                                                }
        """
        keys1, keys2 = set(dict1), set(dict2)

        # Find keys that are different
        diff_keys = {
            k: {
                "old_value": dict1.get(k),
                "new_value": dict2.get(k)
            }
            for k in keys1 | keys2
            if (k not in dict1) or (k not in dict2) or dict1[k] != dict2[k]
        }
        return diff_keys
