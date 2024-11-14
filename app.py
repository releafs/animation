import json
import streamlit as st
import base64

# Load and modify your Lottie JSON data
# ... [same as before]

# Convert JSON data to base64
json_str = json.dumps(modified_json)
json_base64 = base64.b64encode(json_str.encode()).decode()

# Embed the Lottie animation using HTML
html_code = f'''
<div id="lottie"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.7.6/lottie.min.js"></script>
<script>
    var animationData = JSON.parse(atob("{json_base64}"));
    var params = {{
        container: document.getElementById('lottie'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: animationData
    }};
    lottie.loadAnimation(params);
</script>
'''

st.components.v1.html(html_code, height=400, width=700)
