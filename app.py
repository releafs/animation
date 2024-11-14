import json
import streamlit as st
import base64
from streamlit_lottie import st_lottie

# Load JSON from 'tree.json'
def load_json(filepath="tree.json"):
    with open(filepath, "r") as f:
        return json.load(f)

# Save modified JSON to 'tree_modified.json'
def save_json(json_data, filepath="tree_modified.json"):
    with open(filepath, "w") as f:
        json.dump(json_data, f, indent=4)

# Display JSON editor for user modification
def display_json_editor(json_data):
    st.sidebar.header("Edit Tree Animation Parameters")
    
    for index, layer in enumerate(json_data.get("layers", [])):
        if "tree" in layer.get("nm", "").lower():
            st.sidebar.subheader(f"Tree Layer {index + 1}")

            # Adjust position (x, y)
            position = layer["ks"]["p"]["k"]
            layer["ks"]["p"]["k"][0] = st.sidebar.slider(f"Tree {index + 1} X", 0, 1600, int(position[0]), step=10)
            layer["ks"]["p"]["k"][1] = st.sidebar.slider(f"Tree {index + 1} Y", 0, 1200, int(position[1]), step=10)

            # Adjust scale
            scale = layer["ks"]["s"]["k"]
            new_scale = st.sidebar.slider(f"Tree {index + 1} Scale", 50, 300, int(scale[0]), step=10)
            layer["ks"]["s"]["k"] = [new_scale, new_scale, 100]

    return json_data

# Render Lottie JSON
def render_lottie(json_data):
    st.subheader("Live Animation Preview")
    try:
        st_lottie(json_data, height=400, key="lottie_animation")
    except Exception as e:
        st.error("Error rendering Lottie animation. Please check JSON structure.")
        st.write(e)

# Main Streamlit app
def main():
    st.title("Interactive Tree Animation Editor")

    # Load JSON data
    json_data = load_json()
    st.json(json_data)  # Display initial JSON structure

    # Editable JSON in sidebar
    modified_json = display_json_editor(json_data)

    # Save changes back to JSON file
    save_json(modified_json)

    # Render modified Lottie animation
    render_lottie(modified_json)

    st.write("Modified JSON structure has been saved to 'tree_modified.json'.")

if __name__ == "__main__":
    main()
