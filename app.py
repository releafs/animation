import json
import streamlit as st
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor with Map", layout="wide")

# Load the JSON file (tree.json)
@st.cache(allow_output_mutation=True)
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Count the number of trees and collect their labels and positions
def count_trees_with_labels_and_positions(json_data):
    """
    Count the number of tree objects in the animation JSON and collect their labels and positions.
    Returns a count, a list of labels, and a list of positions.
    """
    tree_count = 0
    tree_labels = []
    tree_positions = []
    
    for layer in json_data.get("layers", []):
        # Check if the layer is named "tree" or contains tree objects
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, count the individual shapes and use layer name as a prefix
            if "shapes" in layer:
                shape_count = len(layer["shapes"])
                tree_count += shape_count
                for i, shape in enumerate(layer["shapes"]):
                    tree_labels.append(f"{layer['nm']} - Shape {i+1}")
                    # Default position for each shape if available
                    tree_positions.append(layer["ks"]["p"]["k"])
            else:
                tree_count += 1
                tree_labels.append(layer["nm"])
                tree_positions.append(layer["ks"]["p"]["k"])  # Default position for a single tree

    return tree_count, tree_labels, tree_positions

# Function to display the position map
def display_position_map(tree_positions, tree_labels, visibility):
    """
    Displays a map of tree positions based on their coordinates.
    """
    # Filter positions based on visibility
    visible_positions = [pos for pos, vis in zip(tree_positions, visibility) if vis]
    visible_labels = [label for label, vis in zip(tree_labels, visibility) if vis]

    fig, ax = plt.subplots(figsize=(8, 6))
    for pos, label in zip(visible_positions, visible_labels):
        ax.scatter(pos[0], pos[1], label=label)

    ax.set_title("Tree Position Map")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0), fontsize="small")
    st.pyplot(fig)

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the number of trees, their labels, and positions
    tree_count, tree_labels, tree_positions = count_trees_with_labels_and_positions(json_data)
    st.sidebar.info(f"Number of Trees: {tree_count}")

    # Sidebar for toggling visibility
    st.sidebar.subheader("Tree Visibility")
    visibility = [st.sidebar.checkbox(label, value=True) for label in tree_labels]

    # Apply button
    apply_changes = st.sidebar.button("Apply Changes")

    # If Apply is clicked, refresh the view
    if apply_changes:
        st.experimental_rerun()

    # Display position map
    st.subheader("Tree Position Map")
    display_position_map(tree_positions, tree_labels, visibility)

    # Edit position and scale for visible trees
    st.sidebar.subheader("Tree Parameters")
    for index, (label, pos, vis) in enumerate(zip(tree_labels, tree_positions, visibility)):
        if vis:  # Only display sliders for visible trees
            st.sidebar.subheader(f"Edit {label}")

            # Edit position (x, y)
            new_x = st.sidebar.slider(f"{label} Position X", 0, 1600, int(pos[0]), step=10)
            new_y = st.sidebar.slider(f"{label} Position Y", 0, 1200, int(pos[1]), step=10)
            updated_json["layers"][index]["ks"]["p"]["k"] = [new_x, new_y, pos[2]]

            # Edit scale
            scale = updated_json["layers"][index]["ks"]["s"]["k"]
            new_scale = st.sidebar.slider(f"{label} Scale", 50, 300, int(scale[0]), step=10)
            updated_json["layers"][index]["ks"]["s"]["k"] = [new_scale, new_scale, 100]

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor with Position Map")
    st.markdown("Use the sidebar to adjust the tree animation parameters and toggle tree visibility.")

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
