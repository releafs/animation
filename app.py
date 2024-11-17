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
        if "tree" in layer.get("nm", "").lower():
            if "shapes" in layer:
                tree_count += len(layer["shapes"])  # Count shapes as individual trees
            else:
                tree_count += 1  # Count the layer as one tree if no shapes found

    return tree_count

# Modify the JSON to display the specified number of trees
def modify_tree_count(json_data, num_trees):
    """
    Modify the JSON to show only the specified number of trees.
    """
    modified_json = json_data.copy()
    current_tree_count = count_trees(modified_json)
    
    # Adjust layers or shapes to limit the number of trees
    tree_layers = [layer for layer in modified_json["layers"] if "tree" in layer.get("nm", "").lower()]
    
    if len(tree_layers) > 0:
        # Check if trees are in layers or shapes
        for layer in tree_layers:
            if "shapes" in layer:
                # Modify shapes to limit the count
                layer["shapes"] = layer["shapes"][:num_trees]  # Keep only the first num_trees shapes
                num_trees -= len(layer["shapes"])  # Reduce the remaining count to handle next layer
            else:
                if num_trees <= 0:
                    modified_json["layers"].remove(layer)  # Remove extra layers if not needed
                num_trees -= 1

    return modified_json

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data, num_trees):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Display editable tree count
    tree_count = count_trees(updated_json)
    st.sidebar.info(f"Number of Trees: {tree_count}")
    num_trees = st.sidebar.slider("Adjust Number of Trees", 1, tree_count, value=num_trees)

    # Modify JSON to limit tree count
    updated_json = modify_tree_count(updated_json, num_trees)

    # Edit position and scale of the first few trees
    tree_layers = [layer for layer in updated_json["layers"] if "tree" in layer.get("nm", "").lower()]
    for index, layer in enumerate(tree_layers[:num_trees]):
        st.sidebar.subheader(f"Tree {index + 1}")
        position = layer["ks"]["p"]["k"]
        new_x = st.sidebar.slider(f"Tree {index + 1} Position X", 0, 1600, int(position[0]), step=10)
        new_y = st.sidebar.slider(f"Tree {index + 1} Position Y", 0, 1200, int(position[1]), step=10)
        layer["ks"]["p"]["k"] = [new_x, new_y, position[2]]

        scale = layer["ks"]["s"]["k"]
        new_scale = st.sidebar.slider(f"Tree {index + 1} Scale", 50, 300, int(scale[0]), step=10)
        layer["ks"]["s"]["k"] = [new_scale, new_scale, 100]

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters.")

    # Load JSON data from tree.json
    json_data = load_json()

    # Initial number of trees to display
    num_trees = count_trees(json_data)

    # Display editable parameters in sidebar and apply changes
    modified_json = display_json_editor(json_data, num_trees)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
