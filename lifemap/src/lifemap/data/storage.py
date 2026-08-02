from typing import Any, Dict
import json
import os

class Storage:
    def __init__(self, storage_file: str):
        self.storage_file = storage_file
        self.data = self.load_data()

    def load_data(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self) -> None:
        with open(self.storage_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_entry(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save_data()

    def get_entry(self, key: str) -> Any:
        return self.data.get(key)

    def remove_entry(self, key: str) -> None:
        if key in self.data:
            del self.data[key]
            self.save_data()