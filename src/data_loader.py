import json

class DataLoader:
    def load_json(self, filename: str) -> list:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file {filename}")
        