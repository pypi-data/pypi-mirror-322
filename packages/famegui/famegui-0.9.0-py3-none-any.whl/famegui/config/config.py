import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

parent_dir = os.path.dirname(BASE_DIR)

DEFAULT_FAME_WORK_DIR = os.path.join(parent_dir, "testing_resources")

CUSTOM_DELIVERY_STEPS_TIME_OPTION = "Custom"
