import json
import copy
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
        if "tree" in layer.get("nm", "").lower():
            if "shapes" in layer:
                tree_count += len(layer["shapes"])
            else:
                tree_count += 1
    return tree_count

# Add a new tree layer
def add_tree(json_data, initial_tree_count):
    """
    Add a new tree by duplicating an existing tree layer.
    """
    # Find the first tree layer to duplicate
    for layer in json_data["layers"]:
        if "tree" in layer.get("nm", "").lower():
            new_tree = copy.deepcopy(layer)  # Duplicate the first tree layer
            new_tree["nm"] = f"tree_{initial_tree_count + 1}"  # Rename based on count
            new_tree["ks"]["p"]["k"] = [new_tree["ks"]["p"]["k"][0] + 50,  # Offset X
                                        new_tree["ks"]["p"]["k"][1] + 50,  # Offset Y
                                        new_tree["ks"]["p"]["k"][2]]  # Keep Z unchanged
            json_data["layers"].append(new_tree)  # Add the new tree to the layers
            break
    return json_data

# Remove the last tree layer
def remove_tree(json_data, initial_tree_count):
    """
    Remove the last tree layer.
    """
    # Iterate layers in reverse order to find the last tree layer
    for i in range(len(json_data["layers"]) - 1, -1, -1):
        if "tree" in json_data["layers"][i].get("nm", "").lower():
            current_tree_count = count_trees(json_data)
            if current_tree_count > initial_tree_count:  # Only remove if above baseline
                del json_data["layers"][i]
                break
    return json_data

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data, initial_tree_count):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Display the number of trees
    tree_count = count_trees(json_data)
    st.sidebar.info(f"Number of Trees: {tree_count}")

    # Add and Remove buttons
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Add Tree"):
        updated_json = add_tree(updated_json, tree_count)
    if col2.button("Remove Tree"):
        if tree_count > initial_tree_count:  # Only remove if above baseline
            updated_json = remove_tree(updated_json, initial_tree_count)

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

    # Get the initial tree count
    initial_tree_count = count_trees(json_data)

    # Display editable parameters in sidebar and apply changes
    modified_json = display_json_editor(json_data, initial_tree_count)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
