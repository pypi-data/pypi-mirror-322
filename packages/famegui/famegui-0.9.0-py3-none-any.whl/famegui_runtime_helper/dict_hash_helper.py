import hashlib
import ujson as json


def hash_dict(d):
    """Generate a consistent hash for a dictionary."""
    # Serialize the dictionary into a sorted JSON string
    serialized = json.dumps(d, sort_keys=True)
    # Hash the serialized string
    return hashlib.sha256(serialized.encode()).hexdigest()
