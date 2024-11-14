import json
import streamlit as st
import base64
import copy

# Load JSON from tree.json
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Function to convert JSON to a base64 string for embedding
def json_to_base64(json_data):
    json_str = json.dumps(json_data)
    return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')

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
            # Ensure the position list has at least 2 elements
            if len(position) >= 2:
                layer["ks"]["p"]["k"] = [new_x, new_y] + position[2:]
            else:
                layer["ks"]["p"]["k"] = [new_x, new_y]

            # Edit scale
            scale = layer["ks"]["s"]["k"]
            new_scale = st.sidebar.slider(f"Tree {index + 1} Scale", 50, 300, int(scale[0]), step=10)
            # Ensure the scale list has at least 2 elements
            if len(scale) >= 2:
                layer["ks"]["s"]["k"] = [new_scale, new_scale] + scale[2:]
            else:
                layer["ks"]["s"]["k"] = [new_scale, new_scale]

            updated_json["layers"][index] = layer

    return updated_json

# Function to render Lottie animation as an HTML component
def render_lottie_html(json_data):
    base64_json = json_to_base64(json_data)
    html_code = f'''
    <div id="lottie-animation" style="width:100%; height:400px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.7.4/lottie.min.js"></script>
    <script>
        var animationData = JSON.parse(atob("{base64_json}"));
        var params = {{
            container: document.getElementById('lottie-animation'),
            renderer: 'svg',
            loop: true,
            autoplay: true,
            animationData: animationData
        }};
        lottie.loadAnimation(params);
    </script>
    '''
    # Use Streamlit to load the HTML
    st.components.v1.html(html_code, height=450)

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

# Run the Streamlit app
if __name__ == "__main__":
    main()
