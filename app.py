import json
import random
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
    return sum(1 for layer in json_data.get("layers", []) if "tree" in layer.get("nm", "").lower())

# Add or remove trees based on user input
def adjust_tree_count(json_data, target_tree_count):
    updated_json = json_data.copy()
    current_tree_count = count_trees(updated_json)
    
    if target_tree_count > current_tree_count:
        # Add new trees
        for i in range(target_tree_count - current_tree_count):
            new_tree = {
                "nm": f"tree_{current_tree_count + i + 1}",
                "ks": {
                    "p": {"k": [random.randint(0, 1600), random.randint(0, 1200), 0]},  # Random position
                    "s": {"k": [100, 100, 100]},  # Default scale
                },
                "shapes": []  # Add shapes if needed
            }
            updated_json["layers"].append(new_tree)
    elif target_tree_count < current_tree_count:
        # Remove excess trees
        updated_json["layers"] = [
            layer for layer in updated_json["layers"] if "tree" not in layer.get("nm", "").lower()
        ][:target_tree_count] + [
            layer for layer in updated_json["layers"] if "tree" not in layer.get("nm", "").lower()
        ]

    return updated_json

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()
    st.sidebar.header("Edit Tree Animation Parameters")

    # Editable number of trees
    current_tree_count = count_trees(updated_json)
    target_tree_count = st.sidebar.number_input(
        "Number of Trees", min_value=0, value=current_tree_count, step=1
    )
    updated_json = adjust_tree_count(updated_json, target_tree_count)

    # Collective controls for all trees
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
