import json
import os.path
from dataclasses import dataclass


@dataclass
class Keys:
    settings8_raw: str
    cricutdevice_request_key: bytes

    @classmethod
    def load(cls, config_root):
        path = os.path.join(config_root, "keys.json")
        if not os.path.exists(path):
            return None

        with open(path) as config_file:
            saved = json.load(config_file)

        if (version := saved.get("version")) != 1:
            raise ValueError(f"wrong keys.json version {version}")

        return cls(
            settings8_raw=saved["settings8_raw"],
            cricutdevice_request_key=bytes.fromhex(saved["cricutdevice_request_key"]),
        )

    def save(self, config_root):
        path = os.path.join(config_root, "keys.json")

        with open(path, "w") as config_file:
            json.dump(
                {
                    "version": 1,
                    "settings8_raw": self.settings8_raw,
                    "cricutdevice_request_key": self.cricutdevice_request_key.hex(),
                },
                config_file,
                indent=4,
            )
