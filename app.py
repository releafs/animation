import json
import streamlit as st
from streamlit_lottie import st_lottie
import copy

# Configure Streamlit page
st.set_page_config(page_title="Duplicate and Offset Tree Animation with Zoom", layout="wide")

# Load the JSON file (modified_tree_animation.json) with st.cache_data
@st.cache_data
def load_json():
    """
    Load the modified JSON file for visualization.
    """
    with open("modified_tree_animation.json", "r") as f:
        return json.load(f)

# Duplicate, apply offsets, and zoom
def apply_transformations(json_data, num_duplicates, offsets, zoom_level):
    """
    Create duplicates of the animation with specified offsets and apply zoom.
    """
    transformed_data = copy.deepcopy(json_data)

    # Apply zoom to all layers
    for layer in transformed_data.get("layers", []):
        if "ks" in layer and "s" in layer["ks"]:  # Check if layer has a scale property
            scale = layer["ks"]["s"]["k"]
            layer["ks"]["s"]["k"] = [scale[0] * zoom_level, scale[1] * zoom_level, scale[2]]

    # Duplicate the layers for each copy
    for i in range(1, num_duplicates + 1):
        for layer in json_data.get("layers", []):
            # Create a duplicate of the layer
            duplicated_layer = copy.deepcopy(layer)
            duplicated_layer["nm"] = f"{layer['nm']} - Copy {i}"  # Update the name for the duplicate
            
            # Apply offsets to position
            if "ks" in duplicated_layer and "p" in duplicated_layer["ks"]:
                duplicated_layer["ks"]["p"]["k"][0] += offsets["x"] * i  # Offset X
                duplicated_layer["ks"]["p"]["k"][1] += offsets["y"] * i  # Offset Y
            
            # Add the duplicated layer to the layers
            transformed_data["layers"].append(duplicated_layer)

    return transformed_data

# Main Streamlit app function
def main():
    st.title("Duplicate and Offset Tree Animation with Zoom")
    st.markdown("Use the sidebar to control the number of duplicates, offsets, and zoom level.")

    # Load JSON data from modified_tree_animation.json
    json_data = load_json()

    # Sidebar controls
    st.sidebar.header("Settings")
    num_duplicates = st.sidebar.number_input(
        "Number of Duplicates", min_value=0, max_value=10, value=2, step=1
    )
    offset_x = st.sidebar.number_input(
        "Offset X (pixels)", min_value=-500, max_value=500, value=100, step=10
    )
    offset_y = st.sidebar.number_input(
        "Offset Y (pixels)", min_value=-500, max_value=500, value=100, step=10
    )
    zoom_level = st.sidebar.number_input(
        "Zoom Level (scale factor)", min_value=0.1, max_value=3.0, value=1.0, step=0.1
    )

    # Prepare offsets and zoom
    offsets = {"x": offset_x, "y": offset_y}

    # Apply transformations
    transformed_json = apply_transformations(json_data, num_duplicates, offsets, zoom_level)

    # Render the transformed JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(transformed_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
