import json
import streamlit as st
from streamlit_lottie import st_lottie
import copy

# Load Lottie JSON file without caching
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.title("Interactive Tree Animation Editor")

# Load and copy the JSON data
original_json = load_lottiefile("tree.json")
modified_json = copy.deepcopy(original_json)

# Sidebar controls
st.sidebar.header("Edit Tree Animation Parameters")

# Loop through each tree layer in the JSON "layers"
for index, layer in enumerate(modified_json.get("layers", [])):
    if "tree" in layer.get("nm", ""):
        st.sidebar.subheader(f"Tree {index + 1}")

        # Edit position (x, y)
        position = layer["ks"]["p"]["k"]
        new_x = st.sidebar.slider(f"Tree {index + 1} Position X", 0, 1600, int(position[0]), step=10)
        new_y = st.sidebar.slider(f"Tree {index + 1} Position Y", 0, 1200, int(position[1]), step=10)
        layer["ks"]["p"]["k"] = [new_x, new_y]

        # Edit scale
        scale = layer["ks"]["s"]["k"]
        new_scale = st.sidebar.slider(f"Tree {index + 1} Scale", 50, 300, int(scale[0]), step=10)
        layer["ks"]["s"]["k"] = [new_scale, new_scale, scale[2]]

        modified_json["layers"][index] = layer

# Display the modified animation with a dynamic key
st_lottie(modified_json, height=400, key=str(modified_json))

# Optionally, display the modified JSON for debugging
st.subheader("Modified JSON Structure")
st.json(modified_json)
