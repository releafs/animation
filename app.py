import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")

# Allowed shape indices
ALLOWED_SHAPES = [7, 9, 10, 11, 14, 15, 17, 19, 20, 21, 22, 25]

# Default position and scale for "rows of trees"
DEFAULT_POSITION_X = 1160
DEFAULT_POSITION_Y = 710
DEFAULT_SCALE = 400

# Load the JSON file (tree.json) with st.cache_data
@st.cache_data
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Filter tree shapes in the JSON based on ALLOWED_SHAPES and set default values
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

# Duplicate the animation based on the number of copies
def duplicate_animation(json_data, copies, offsets):
    """
    Duplicates the animation `copies` times and adjusts their positions based on offsets.
    """
    duplicated_data = {"layers": []}

    for i in range(copies):
        for layer in json_data.get("layers", []):
            # Create a copy of the layer
            new_layer = layer.copy()
            
            # Adjust position for each duplicate
            if "ks" in new_layer and "p" in new_layer["ks"]:
                x_offset = offsets[i]["x"]
                y_offset = offsets[i]["y"]
                new_layer["ks"]["p"]["k"] = [
                    new_layer["ks"]["p"]["k"][0] + x_offset,
                    new_layer["ks"]["p"]["k"][1] + y_offset,
                    0
                ]
            
            # Add the modified layer to the new animation
            duplicated_data["layers"].append(new_layer)
    return duplicated_data

# Main Streamlit app function
def main():
    st.title("Tree Animation Builder")
    st.markdown("Duplicate and position animations like Lego blocks.")

    # Load JSON data from tree.json
    json_data = load_json()

    # Prepare the base animation
    base_animation = prepare_json(json_data)

    # Sidebar controls for duplication
    st.sidebar.header("Animation Controls")
    copies = st.sidebar.number_input("Number of Animations", min_value=1, max_value=10, value=1, step=1)

    # Collect offsets for each duplicate
    offsets = []
    for i in range(copies):
        st.sidebar.subheader(f"Animation {i + 1} Position")
        x_offset = st.sidebar.slider(f"X Offset for Animation {i + 1}", -2000, 2000, 0, step=10)
        y_offset = st.sidebar.slider(f"Y Offset for Animation {i + 1}", -2000, 2000, 0, step=10)
        offsets.append({"x": x_offset, "y": y_offset})

    # Duplicate animations with specified offsets
    final_animation = duplicate_animation(base_animation, copies, offsets)

    # Render the final animation
    st.subheader("Live Animation Preview")
    st_lottie(final_animation, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
