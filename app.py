import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(layout="wide")

API_URL = st.secrets["API_URL"]

st.title("📸 EventLens - Find Yourself in Wedding Photos")

# Initialize session state
if "image_captured" not in st.session_state:
    st.session_state.image_captured = False
if "img_str" not in st.session_state:
    st.session_state.img_str = None

# Sidebar UI
st.sidebar.header("User Profile")

# 👉 STEP 1: Show camera ONLY if no image captured
if not st.session_state.image_captured:
    img_file_buffer = st.sidebar.camera_input("Take a selfie")

    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)

        # Convert to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        st.session_state.img_str = base64.b64encode(buffered.getvalue()).decode()

        # Save image + freeze state
        st.session_state.image = image
        st.session_state.image_captured = True
        st.rerun()

# 👉 STEP 2: Show captured image + actions
else:
    st.sidebar.image(
        st.session_state.image,
        caption="Captured Selfie",
        use_container_width=True
    )

    col1, col2 = st.sidebar.columns(2)

    # 🔄 Retake button
    with col1:
        if st.button("🔄 Retake"):
            st.session_state.image_captured = False
            st.session_state.img_str = None
            st.rerun()

    # 🔍 Search button
    with col2:
        if st.button("🔍 Search"):
            st.session_state.search_clicked = True

# 👉 SEARCH RESULTS
if st.session_state.get("search_clicked"):
    with st.spinner("Searching for matches..."):
        try:
            response = requests.post(
                API_URL,
                json={"image": st.session_state.img_str}
            )

            if response.status_code == 200:
                results = response.json()

                if not results:
                    st.warning("No matching photos found 😔")
                else:
                    st.success(f"Found {len(results)} matching photos 🎉")

                    # Grid layout
                    cols = st.columns(3)
                    for i, img_url in enumerate(results):
                        with cols[i % 3]:
                            st.image(img_url, use_container_width=True)

            else:
                st.error(f"Error {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error("API request failed")
            st.write(str(e))
