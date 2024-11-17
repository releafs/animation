import json
import streamlit as st
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")

# Load the JSON file (tree.json)
@st.cache(allow_output_mutation=True)
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Count the number of trees and collect their labels and positions
def count_trees_with_positions(json_data):
    """
    Count the number of tree objects in the animation JSON, collect their labels, and extract positions.
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
                for i in range(shape_count):
                    tree_labels.append(f"{layer['nm']} - Shape {i+1}")
                    # Append the layer's position for mapping
                    tree_positions.append(layer["ks"]["p"]["k"])
            else:
                tree_count += 1
                tree_labels.append(layer["nm"])
                # Append the layer's position for mapping
                tree_positions.append(layer["ks"]["p"]["k"])

    return tree_count, tree_labels, tree_positions

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the number of trees, their labels, and positions
    tree_count, tree_labels, tree_positions = count_trees_with_positions(json_data)
    st.sidebar.info(f"Number of Trees: {tree_count}")

    # Display tree labels
    st.sidebar.subheader("Tree Labels")
    for label in tree_labels:
        st.sidebar.text(f"- {label}")

    # Loop through each "tree" in the JSON "layers"
    for index, layer in enumerate(updated_json.get("layers", [])):
        if "tree" in layer.get("nm", ""):  # Check if layer is a tree layer
            st.sidebar.subheader(f"Edit {layer['nm']}")

            # Edit position (x, y)
            position = layer["ks"]["p"]["k"]
            new_x = st.sidebar.slider(f"{layer['nm']} Position X", 0, 1600, int(position[0]), step=10)
            new_y = st.sidebar.slider(f"{layer['nm']} Position Y", 0, 1200, int(position[1]), step=10)
            layer["ks"]["p"]["k"] = [new_x, new_y, position[2]]

            # Edit scale
            scale = layer["ks"]["s"]["k"]
            new_scale = st.sidebar.slider(f"{layer['nm']} Scale", 50, 300, int(scale[0]), step=10)
            layer["ks"]["s"]["k"] = [new_scale, new_scale, 100]

            # Update the layer in the JSON data
            updated_json["layers"][index] = layer

    return updated_json, tree_positions

# Plot the position map of trees
def plot_tree_positions(positions, labels):
    fig, ax = plt.subplots(figsize=(10, 8))
    for idx, (pos, label) in enumerate(zip(positions, labels)):
        ax.scatter(pos[0], pos[1], label=f"{label}", alpha=0.8, edgecolors='k', s=100)
        ax.text(pos[0] + 10, pos[1] + 10, f"{label}", fontsize=8)
    
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 1200)
    ax.set_title("Tree Position Map", fontsize=16)
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.grid(True)
    plt.gca().invert_yaxis()  # Match animation's coordinate system (Y-axis inverted)
    return fig

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters.")

    # Load JSON data from tree.json
    json_data = load_json()
    
    # Display editable parameters in sidebar and apply changes
    modified_json, tree_positions = display_json_editor(json_data)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

    # Plot the tree positions on a map
    st.subheader("Tree Position Map")
    _, tree_labels, _ = count_trees_with_positions(json_data)
    tree_map = plot_tree_positions(tree_positions, tree_labels)
    st.pyplot(tree_map)

# Run the Streamlit app
if __name__ == "__main__":
    main()
