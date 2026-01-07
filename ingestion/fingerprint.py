import json
import os
from datetime import datetime
import hashlib

REGISTRY_PATH = "registry/file_registry.json"

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {}
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(registry: dict):
    os.makedirs("registry", exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def is_file_registered(fingerprint: str) -> bool:
    registry = load_registry()
    return fingerprint in registry


def register_file(fingerprint: str, metadata: dict):
    registry = load_registry()
    registry[fingerprint] = metadata
    save_registry(registry)

def compute_file_fingerprint(file_path: str) -> str:
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()
