import json
import streamlit as st
from streamlit_lottie import st_lottie
import copy

# Configure Streamlit page
st.set_page_config(page_title="Duplicate, Offset, and Scale Tree Animation", layout="wide")

# Load the JSON file (modified_tree_animation.json) with st.cache_data
@st.cache_data
def load_json():
    """
    Load the modified JSON file for visualization.
    """
    with open("modified_tree_animation.json", "r") as f:
        return json.load(f)

# Duplicate, apply offsets, and scale
def apply_transformations(json_data, num_duplicates, offsets, scale):
    """
    Create duplicates of the animation with specified offsets and scaling.
    """
    transformed_data = copy.deepcopy(json_data)

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

            # Apply scaling to the layer
            if "ks" in duplicated_layer and "s" in duplicated_layer["ks"]:
                duplicated_layer["ks"]["s"]["k"][0] = int(duplicated_layer["ks"]["s"]["k"][0] * scale)  # Scale X
                duplicated_layer["ks"]["s"]["k"][1] = int(duplicated_layer["ks"]["s"]["k"][1] * scale)  # Scale Y

            # Add the duplicated layer to the layers
            transformed_data["layers"].append(duplicated_layer)

    return transformed_data

# Main Streamlit app function
def main():
    st.title("Duplicate, Offset, and Scale Tree Animation")
    st.markdown("Use the sidebar to control the number of duplicates, offsets, and scaling.")

    # Load JSON data from modified_tree_animation.json
    json_data = load_json()

    # Sidebar controls
    st.sidebar.header("Duplication and Transformation Settings")
    num_duplicates = st.sidebar.number_input(
        "Number of Duplicates", min_value=0, max_value=10, value=2, step=1
    )
    offset_x = st.sidebar.number_input(
        "Offset X (pixels)", min_value=-500, max_value=500, value=100, step=10
    )
    offset_y = st.sidebar.number_input(
        "Offset Y (pixels)", min_value=-500, max_value=500, value=100, step=10
    )
    scale = st.sidebar.number_input(
        "Scale Factor", min_value=0.1, max_value=5.0, value=1.0, step=0.1
    )

    # Prepare transformations dictionary
    offsets = {"x": offset_x, "y": offset_y}

    # Apply transformations (duplication, offsets, and scaling)
    modified_json = apply_transformations(json_data, num_duplicates, offsets, scale)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
