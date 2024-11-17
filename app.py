import json
import streamlit as st
from streamlit_lottie import st_lottie
import copy

# Configure Streamlit page
st.set_page_config(page_title="Duplicate and Offset Tree Animation", layout="wide")

# Load the JSON file (modified_tree_animation.json) with st.cache_data
@st.cache_data
def load_json():
    """
    Load the modified JSON file for visualization.
    """
    with open("modified_tree_animation.json", "r") as f:
        return json.load(f)

# Duplicate and apply offsets
def apply_offsets(json_data, num_duplicates, offsets):
    """
    Create duplicates of the animation with specified offsets.
    """
    duplicated_data = copy.deepcopy(json_data)

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
            duplicated_data["layers"].append(duplicated_layer)

    return duplicated_data

# Main Streamlit app function
def main():
    st.title("Duplicate and Offset Tree Animation")
    st.markdown("Use the sidebar to control the number of duplicates and their offsets.")

    # Load JSON data from modified_tree_animation.json
    json_data = load_json()

    # Sidebar controls
    st.sidebar.header("Duplication Settings")
    num_duplicates = st.sidebar.slider("Number of Duplicates", min_value=0, max_value=10, value=2, step=1)
    offset_x = st.sidebar.slider("Offset X (pixels)", min_value=-500, max_value=500, value=100, step=10)
    offset_y = st.sidebar.slider("Offset Y (pixels)", min_value=-500, max_value=500, value=100, step=10)

    # Prepare offsets dictionary
    offsets = {"x": offset_x, "y": offset_y}

    # Apply duplication and offsets
    modified_json = apply_offsets(json_data, num_duplicates, offsets)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
