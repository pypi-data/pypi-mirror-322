import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

CACHE_DIR = os.path.join(PROJECT_DIR, "cache")

os.makedirs(CACHE_DIR, exist_ok=True)

CACHE_TRACKING_DB_DIR = os.path.join(CACHE_DIR, "db")

CACHE_TRACKING_DB_PATH = os.path.join(CACHE_TRACKING_DB_DIR, "db.json")
