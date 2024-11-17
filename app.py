import json
import streamlit as st
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")

# Load the JSON file (tree.json)
@st.cache(allow_output_mutation=True)
def load_json():import json
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

    # Toggle visibility for each shape
    visibility = []
    st.sidebar.subheader("Toggle Tree Visibility")
    for label in tree_labels:
        is_visible = st.sidebar.checkbox(f"Show {label}", value=True)
        visibility.append(is_visible)

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

    return updated_json, tree_positions, visibility

# Plot the position map of trees
def plot_tree_positions(positions, labels, visibility):
    """
    Plot the position map of trees with proper scaling and labeling.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Extract x and y positions
    for idx, (pos, label, is_visible) in enumerate(zip(positions, labels, visibility)):
        if is_visible:  # Only plot visible trees
            x, y = pos[0], pos[1]
            ax.scatter(x, y, label=f"{label}", alpha=0.8, edgecolors='k', s=100, zorder=3)
            ax.text(x + 10, y + 10, f"{label}", fontsize=8, zorder=4)

    # Set plot limits dynamically
    if positions:
        x_positions = [pos[0] for pos, vis in zip(positions, visibility) if vis]
        y_positions = [pos[1] for pos, vis in zip(positions, visibility) if vis]
        if x_positions and y_positions:
            x_min, x_max = min(x_positions) - 50, max(x_positions) + 50
            y_min, y_max = min(y_positions) - 50, max(y_positions) + 50
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)

    # Set plot title and labels
    ax.set_title("Tree Position Map", fontsize=16)
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.grid(True)

    # Invert y-axis to match animation's coordinate system
    plt.gca().invert_yaxis()

    return fig

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters.")

    # Load JSON data from tree.json
    json_data = load_json()
    
    # Display editable parameters in sidebar and apply changes
    modified_json, tree_positions, visibility = display_json_editor(json_data)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

    # Plot the tree positions on a map
    st.subheader("Tree Position Map")
    _, tree_labels, _ = count_trees_with_positions(json_data)
    tree_map = plot_tree_positions(tree_positions, tree_labels, visibility)
    st.pyplot(tree_map)

# Run the Streamlit app
if __name__ == "__main__":
    main()

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
def plot_tree_positions(positions, labels, x_range, y_range):
    """
    Plot the position map of trees with proper scaling and labeling, allowing dynamic axis range.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Extract x and y positions
    x_positions = [pos[0] for pos in positions]
    y_positions = [pos[1] for pos in positions]

    # Apply user-defined axis limits
    x_min, x_max = x_range
    y_min, y_max = y_range

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Plot each tree position
    for idx, (x, y, label) in enumerate(zip(x_positions, y_positions, labels)):
        ax.scatter(x, y, label=f"{label}", alpha=0.8, edgecolors='k', s=100, zorder=3)
        ax.text(x + 10, y + 10, f"{label}", fontsize=8, zorder=4)

    # Set plot title and labels
    ax.set_title("Tree Position Map", fontsize=16)
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.grid(True)

    # Invert y-axis to match animation's coordinate system
    plt.gca().invert_yaxis()

    return fig

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters.")

    # Load JSON data from tree.json
    json_data = load_json()
    
    # Display editable parameters in sidebar and apply changes
    modified_json, tree_positions = display_json_editor(json_data)

    # Allow user to input custom ranges for X and Y positions
    st.sidebar.header("Map Settings")
    x_min = st.sidebar.number_input("X Position Minimum", value=0, step=10)
    x_max = st.sidebar.number_input("X Position Maximum", value=1600, step=10)
    y_min = st.sidebar.number_input("Y Position Minimum", value=0, step=10)
    y_max = st.sidebar.number_input("Y Position Maximum", value=1200, step=10)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

    # Plot the tree positions on a map
    st.subheader("Tree Position Map")
    _, tree_labels, _ = count_trees_with_positions(json_data)
    tree_map = plot_tree_positions(tree_positions, tree_labels, (x_min, x_max), (y_min, y_max))
    st.pyplot(tree_map)

# Run the Streamlit app
if __name__ == "__main__":
    main()
