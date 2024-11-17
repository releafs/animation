import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")

# Clear the cache when the app is reloaded
@st.cache_data.clear
def clear_cache():
    pass

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
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, count the individual shapes
            if "shapes" in layer:
                tree_count += len(layer["shapes"])  # Each shape could represent a tree
            else:
                tree_count += 1  # Count the layer as one tree if no shapes found
    return tree_count

# Add a new tree layer to the JSON
def add_tree(json_data):
    """
    Add a new tree layer to the animation JSON by duplicating an existing tree layer.
    """
    for layer in json_data.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            new_tree = layer.copy()
            new_tree["nm"] = "tree_copy"  # Rename the tree layer
            new_tree["ks"]["p"]["k"][0] += 50  # Offset position X for uniqueness
            json_data["layers"].append(new_tree)
            break  # Add only one tree

# Remove the last tree layer from the JSON
def remove_tree(json_data):
    """
    Remove the last tree layer from the animation JSON.
    """
    for i in reversed(range(len(json_data.get("layers", [])))):
        if "tree" in json_data["layers"][i].get("nm", "").lower():
            del json_data["layers"][i]
            break  # Remove only one tree

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the number of trees
    tree_count = count_trees(updated_json)
    st.sidebar.info(f"Fixed Number of Trees: 35\nCurrent Trees: {tree_count}")

    # Buttons to add or remove trees
    if st.sidebar.button("Add Tree"):
        add_tree(updated_json)

    if st.sidebar.button("Remove Tree"):
        remove_tree(updated_json)

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

    # Clear the cache when the app starts
    clear_cache()

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
