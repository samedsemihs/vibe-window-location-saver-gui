import json
import os
import sys

from constants import LAYOUTS_DIR


def _layouts_path():
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller .exe - use exe directory
        base = os.path.dirname(sys.executable)
    else:
        # Running from source
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, LAYOUTS_DIR)


def list_layouts():
    """Return sorted list of layout names (without .json extension)."""
    path = _layouts_path()
    if not os.path.isdir(path):
        return []
    return sorted(
        os.path.splitext(f)[0]
        for f in os.listdir(path)
        if f.endswith(".json")
    )


def save_layout(name, data):
    """Save layout data as JSON."""
    path = _layouts_path()
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, f"{name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_layout(name):
    """Load and return layout data from JSON file."""
    filepath = os.path.join(_layouts_path(), f"{name}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_layout(name):
    """Delete a layout file."""
    filepath = os.path.join(_layouts_path(), f"{name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
