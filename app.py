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
def apply_transformations(json_data, num_duplicates, offsets, scale_factor):
    """
    Create duplicates of the animation with specified offsets and apply an overall scale factor.
    """
    transformed_data = copy.deepcopy(json_data)

    # Apply transformations to original and duplicated layers
    for i in range(0, num_duplicates + 1):  # Include the original layer (i=0)
        for layer in json_data.get("layers", []):
            # Create a duplicate of the layer for duplicates only (i > 0)
            transformed_layer = copy.deepcopy(layer) if i > 0 else layer

            if i > 0:
                transformed_layer["nm"] = f"{layer['nm']} - Copy {i}"  # Update the name for the duplicate

            # Apply offsets to position
            if "ks" in transformed_layer and "p" in transformed_layer["ks"]:
                transformed_layer["ks"]["p"]["k"][0] += offsets["x"] * i  # Offset X
                transformed_layer["ks"]["p"]["k"][1] += offsets["y"] * i  # Offset Y

            # Apply overall scaling
            if "ks" in transformed_layer and "s" in transformed_layer["ks"]:
                transformed_layer["ks"]["s"]["k"] = [
                    int(transformed_layer["ks"]["s"]["k"][0] * scale_factor),  # Scale X
                    int(transformed_layer["ks"]["s"]["k"][1] * scale_factor),  # Scale Y
                    100,  # Keep Z scale at 100 (default for 2D animations)
                ]

            # Add duplicates to the layers
            if i > 0:
                transformed_data["layers"].append(transformed_layer)

    return transformed_data

# Main Streamlit app function
def main():
    st.title("Duplicate, Offset, and Scale Tree Animation")
    st.markdown("Use the sidebar to control duplication, offsets, and overall scale.")

    # Load JSON data from modified_tree_animation.json
    json_data = load_json()

    # Sidebar controls
    st.sidebar.header("Transformation Settings")
    num_duplicates = st.sidebar.number_input(
        "Number of Duplicates", min_value=0, max_value=10, value=2, step=1
    )
    offset_x = st.sidebar.number_input(
        "Offset X (pixels)", min_value=-500, max_value=500, value=100, step=10
    )
    offset_y = st.sidebar.number_input(
        "Offset Y (pixels)", min_value=-500, max_value=500, value=100, step=10
    )
    scale_factor = st.sidebar.number_input(
        "Overall Scale Factor", min_value=0.1, max_value=2.0, value=1.0, step=0.1
    )

    # Prepare offsets and transformations
    offsets = {"x": offset_x, "y": offset_y}

    # Apply transformations
    modified_json = apply_transformations(json_data, num_duplicates, offsets, scale_factor)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
