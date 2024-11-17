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

# Modify the JSON to keep only 9 trees in a 3x3 grid
def keep_nine_trees(json_data):
    """
    Modify the JSON to retain only 9 trees arranged in a 3x3 grid.
    """
    updated_json = json_data.copy()

    # Identify tree layers
    tree_layers = [
        layer for layer in updated_json.get("layers", [])
        if "tree" in layer.get("nm", "").lower()
    ]
    
    # Select only the first 9 trees
    selected_trees = tree_layers[:9]

    # Arrange them in a 3x3 grid
    grid_positions = [
        [400, 400], [800, 400], [1200, 400],  # First row
        [400, 800], [800, 800], [1200, 800],  # Second row
        [400, 1200], [800, 1200], [1200, 1200]  # Third row
    ]
    
    for idx, tree in enumerate(selected_trees):
        # Update position to align in 3x3 grid
        tree["ks"]["p"]["k"] = [grid_positions[idx][0], grid_positions[idx][1], 0]

    # Replace the original layers with the updated 9 trees + other non-tree layers
    updated_json["layers"] = selected_trees + [
        layer for layer in updated_json.get("layers", [])
        if "tree" not in layer.get("nm", "").lower()
    ]

    return updated_json

# Count the number of trees in the animation
def count_trees(json_data):
    """
    Count the number of tree objects in the animation JSON.
    """
    tree_count = sum(1 for layer in json_data.get("layers", []) if "tree" in layer.get("nm", "").lower())
    return tree_count

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the number of trees
    tree_count = count_trees(json_data)
    st.sidebar.info(f"Number of Trees: {tree_count}")

    # Loop through each "tree" in the JSON "layers"
    for index, layer in enumerate(updated_json.get("layers", [])):
        if "tree" in layer.get("nm", ""):  # Check if layer is a tree layer
            st.sidebar.subheader(f"Tree {index + 1}")
            
            # Edit position (x, y)
            position = layer["ks"]["p"]["k"]
            new_x = st.sidebar.slider(f"Tree {index + 1} Position X", 0, 1600, int(position[0]), step=10)
            new_y = st.sidebar.slider(f"Tree {index + 1} Position Y", 0, 1200, int(position[1]), step=10)
            layer["ks"]["p"]["k"] = [new_x, new_y, position[2]]

            # Edit scale
            scale = layer["ks"]["s"]["k"]
            new_scale = st.sidebar.slider(f"Tree {index + 1} Scale", 50, 300, int(scale[0]), step=10)
            layer["ks"]["s"]["k"] = [new_scale, new_scale, 100]

            # Update the layer in the JSON data
            updated_json["layers"][index] = layer

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters.")

    # Load JSON data from tree.json
    json_data = load_json()
    
    # Modify JSON to keep only 9 trees
    json_data = keep_nine_trees(json_data)

    # Display editable parameters in sidebar and apply changes
    modified_json = display_json_editor(json_data)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
