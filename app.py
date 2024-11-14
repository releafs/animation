import json
import copy
import streamlit as st
import base64

# Load JSON from tree.json
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Function to render Lottie animation as an HTML component
def render_lottie_html(json_data):
    base64_json = base64.b64encode(json.dumps(json_data).encode()).decode()
    html_code = f'''
    <div id="lottie-animation" style="width:100%; height:400px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.7.6/lottie.min.js"></script>
    <script>
        const animationData = JSON.parse(atob("{base64_json}"));
        lottie.loadAnimation({{
            container: document.getElementById('lottie-animation'),
            renderer: 'svg',
            loop: true,
            autoplay: true,
            animationData: animationData
        }});
    </script>
    '''
    st.components.v1.html(html_code, height=450, scrolling=True, unsafe_allow_html=True)

# Display JSON parameters for editing
def display_json_editor(json_data):
    updated_json = copy.deepcopy(json_data)
    st.sidebar.header("Edit Tree Animation Parameters")

    # Loop through each tree layer in the JSON "layers"
    for index, layer in enumerate(updated_json.get("layers", [])):
        if "tree" in layer.get("nm", "").lower():
            st.sidebar.subheader(f"Tree {index + 1}")

            # Edit position (x, y)
            position = layer["ks"]["p"]["k"]
            new_x = st.sidebar.slider(f"Tree {index + 1} Position X", 0, 1600, int(position[0]), step=10)
            new_y = st.sidebar.slider(f"Tree {index + 1} Position Y", 0, 1200, int(position[1]), step=10)
            layer["ks"]["p"]["k"] = [new_x, new_y, position[2]]

            # Edit scale
            scale = layer["ks"]["s"]["k"]
            new_scale = st.sidebar.slider(f"Tree {index + 1} Scale", 50, 300, int(scale[0]), step=10)
            layer["ks"]["s"]["k"] = [new_scale, new_scale, 100]

            updated_json["layers"][index] = layer

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")

    # Load JSON data from tree.json
    json_data = load_json()

    # Display editable parameters in sidebar and apply changes
    modified_json = display_json_editor(json_data)

    # Display JSON structure for reference
    st.subheader("Modified JSON Structure")
    st.json(modified_json)

    # Render animation using HTML and Lottie Web Player
    st.subheader("Live Animation Preview")
    render_lottie_html(modified_json)

if __name__ == "__main__":
    main()
