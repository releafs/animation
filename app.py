import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Preview", layout="wide")

# Allowed shape indices
ALLOWED_SHAPES = [7, 9, 10, 11, 14, 15, 17, 19, 20, 21, 22, 25]

# Default position and scale for "rows of trees"
DEFAULT_POSITION_X = 1160
DEFAULT_POSITION_Y = 710
DEFAULT_SCALE = 400
DUPLICATE_OFFSET_X = 600  # Offset for duplicated animation

# Load the JSON file (tree.json) with st.cache_data
@st.cache_data
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Filter tree shapes in the JSON based on ALLOWED_SHAPES and set default values
def prepare_json_with_duplicate(json_data):
    """
    Filters the tree shapes to include only those with indices in ALLOWED_SHAPES,
    applies default position and scale for the "rows of trees" layer, and duplicates the animation.
    """
    prepared_data = json_data.copy()
    duplicate_layers = []

    for layer in prepared_data.get("layers", []):
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

                # Create a duplicate of the layer with an offset
                duplicate_layer = layer.copy()
                duplicate_layer["nm"] = f"{layer['nm']} - Copy"
                duplicate_layer["ks"]["p"]["k"] = [
                    DEFAULT_POSITION_X + DUPLICATE_OFFSET_X,
                    DEFAULT_POSITION_Y,
                    0,
                ]
                duplicate_layers.append(duplicate_layer)

    # Add the duplicated layers to the JSON
    prepared_data["layers"].extend(duplicate_layers)
    return prepared_data

# Main Streamlit app function
def main():
    st.title("Duplicated Tree Animation")
    st.markdown("This animation shows two tree animations side by side.")

    # Load JSON data from tree.json
    json_data = load_json()

    # Prepare the JSON with the duplicated animation
    prepared_json = prepare_json_with_duplicate(json_data)

    # Render the prepared JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(prepared_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
