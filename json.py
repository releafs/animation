import json
from streamlit.cache_data import cache_data

# Allowed shape indices
ALLOWED_SHAPES = [7, 9, 10, 11, 14, 15, 17, 19, 20, 21, 22, 25]

# Default position and scale for "rows of trees"
DEFAULT_POSITION_X = 1160
DEFAULT_POSITION_Y = 710
DEFAULT_SCALE = 400

@cache_data
def load_json(file_path="tree.json"):
    """
    Load the JSON file from the specified file path.
    """
    with open(file_path, "r") as f:
        return json.load(f)

def prepare_json(json_data):
    """
    Filters the tree shapes to include only those with indices in ALLOWED_SHAPES
    and applies default position and scale for the "rows of trees" layer.
    """
    filtered_data = json_data.copy()
    
    for layer in filtered_data.get("layers", []):
        # Check if the layer is named "tree" or contains tree objects
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, filter only allowed shapes
            if "shapes" in layer:
                layer["shapes"] = [
                    shape for i, shape in enumerate(layer["shapes"]) if (i + 1) in ALLOWED_SHAPES
                ]
            # Apply default position and scale for "rows of trees"
            if "rows of trees" in layer.get("nm", "").lower():
                layer["ks"]["p"]["k"] = [DEFAULT_POSITION_X, DEFAULT_POSITION_Y, 0]  # Position
                layer["ks"]["s"]["k"] = [DEFAULT_SCALE, DEFAULT_SCALE, 100]  # Scale
    return filtered_data
