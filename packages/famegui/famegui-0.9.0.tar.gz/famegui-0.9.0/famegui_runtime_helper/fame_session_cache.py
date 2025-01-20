from famegui_runtime_helper.dict_hash_helper import hash_dict
from famegui.database.prebuild_queries.consts_from_settings import get_setting_value, FameGeneralRuntimeSetting


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class FameSessionCache(metaclass=SingletonMeta):
    def __init__(self):
        self.MAX_UNDO_STEPS = int(get_setting_value(FameGeneralRuntimeSetting.AMOUNT_OF_UNDO_STEPS, 10))
        if not hasattr(self, 'items'):
            self.items = []
        if not hasattr(self, 'redo_items'):
            self.redo_items = []

    def _is_item_in_list(self, item, my_list):
        item_hash = hash_dict(item)
        for list_item in my_list:
            if hash_dict(list_item) == item_hash:
                return True
        return False

    def add_item(self, item: dict):
        if self._is_item_in_list(item, self.items):
            return

        if not isinstance(item, dict):
            raise ValueError("Item must be a dictionary.")

        if len(self.items) >= self.MAX_UNDO_STEPS:
            self.items.pop(0)

        self.items.append(item)
        self.redo_items = []  # Clear redo history

    def get_last_item(self):
        if not self.items:
            return None

        item = self.items.pop()
        self.redo_items.append(item)
        return item

    def redo_last_item(self):
        if not self.redo_items:
            return None

        item = self.redo_items.pop()
        self.items.append(item)  # Direct append to avoid clearing redo stack
        return item

    def remove_item_by_index(self, index: int):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        raise IndexError("Index out of range.")

    def get_items(self):
        return self.items