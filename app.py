import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation App", layout="wide")

# Load the JSON file (tree.json)
@st.cache(allow_output_mutation=True)
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Count trees and prepare visibility controls
def setup_tree_controls(json_data):
    """
    Prepare a visibility map for individual trees.
    """
    tree_visibility = {}
    for layer in json_data.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            for i, shape in enumerate(layer.get("shapes", [])):
                tree_visibility[i] = True  # Default visibility is True
    return tree_visibility

# Update tree visibility in the JSON
def update_tree_visibility(json_data, visibility_map):
    updated_json = json_data.copy()
    for layer in updated_json.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            for i, shape in enumerate(layer.get("shapes", [])):
                if i in visibility_map and not visibility_map[i]:
                    shape["hd"] = True  # Hide the tree if switched off
                elif i in visibility_map:
                    shape.pop("hd", None)  # Ensure it's visible if switched on
    return updated_json

# Main function for the animation page
def animation_page(json_data):
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters.")

    # Apply visibility controls from session state
    visibility_map = st.session_state.get("visibility_map", {})
    modified_json = update_tree_visibility(json_data, visibility_map)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

    # Link to Tree Control Page
    if st.button("Go to Tree Control Page"):
        st.session_state["current_page"] = "Tree Control"

# Tree control page to manage visibility
def tree_control_page(json_data):
    st.title("Tree Control Page")
    st.markdown("Manage the visibility of trees in the animation.")

    # Initialize visibility map in session state if not already done
    if "visibility_map" not in st.session_state:
        st.session_state["visibility_map"] = setup_tree_controls(json_data)

    # Display tree controls as a table
    visibility_map = st.session_state["visibility_map"]
    st.subheader("Tree Visibility Table")
    for tree_id, is_visible in visibility_map.items():
        visibility_map[tree_id] = st.checkbox(
            f"Tree {tree_id + 1}", value=is_visible, key=f"tree_{tree_id}"
        )

    # Link back to the animation page
    if st.button("Go to Animation Editor"):
        st.session_state["current_page"] = "Animation Editor"

# Main Streamlit app function
def main():
    # Load the JSON file
    json_data = load_json()

    # Initialize session state for page navigation
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Animation Editor"

    # Page navigation
    if st.session_state["current_page"] == "Animation Editor":
        animation_page(json_data)
    elif st.session_state["current_page"] == "Tree Control":
        tree_control_page(json_data)

if __name__ == "__main__":
    main()
