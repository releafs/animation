import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")

# Load the JSON file (tree.json)
@st.cache(allow_output_mutation=True)
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Count the number of trees in the animation
def count_trees(json_data):
    """
    Count the number of tree objects in the animation JSON.
    """
    tree_count = 0
    for layer in json_data.get("layers", []):
        # Check if the layer is named "tree" or contains tree objects
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, count the individual shapes
            if "shapes" in layer:
                tree_count += len(layer["shapes"])  # Each shape could represent a tree
            else:
                tree_count += 1  # Count the layer as one tree if no shapes found

    return tree_count

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the number of trees
    tree_count = count_trees(json_data)
    st.sidebar.info(f"Number of Trees: {tree_count}")

    # Add collective controls for all trees
    st.sidebar.subheader("All Trees Settings")

    # Control collective position offset
    position_offset_x = st.sidebar.slider("All Trees Position Offset X", -500, 500, 0, step=10)
    position_offset_y = st.sidebar.slider("All Trees Position Offset Y", -500, 500, 0, step=10)

    # Control collective scaling factor
    scaling_factor = st.sidebar.slider("All Trees Scale Factor", 50, 300, 100, step=10)

    # Apply these collective settings to all tree layers
    for layer in updated_json.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            # Update position
            position = layer["ks"]["p"]["k"]
            layer["ks"]["p"]["k"] = [
                position[0] + position_offset_x,  # Adjust X
                position[1] + position_offset_y,  # Adjust Y
                position[2],
            ]

            # Update scale
            layer["ks"]["s"]["k"] = [scaling_factor, scaling_factor, 100]

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters.")

    # Load JSON data from tree.json
    json_data = load_json()
    
    # Display editable parameters in sidebar and apply changes
    modified_json = display_json_editor(json_data)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
