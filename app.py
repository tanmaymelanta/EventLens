import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(layout="wide")

API_URL = st.secrets["API_URL"]

st.title("📸 EventLens - Find Yourself in Event")

# Initialize session state
if "valid_user" not in st.session_state:
    st.session_state.valid_user = False
if "image_captured" not in st.session_state:
    st.session_state.image_captured = False
if "img_str" not in st.session_state:
    st.session_state.img_str = None
if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

if not st.session_state.valid_user:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### 🔐 Login")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if username == st.secrets["APP_USERNAME"] and password == st.secrets["APP_PASSWORD"]:
                    st.session_state.valid_user = True
                    st.session_state.user = st.secrets["APP_PROFILE"]

                    st.rerun()
                else:
                    st.error("Invalid credentials")
            st.stop()

# Sidebar UI
st.sidebar.header(f"Welcome {st.session_state.user}")
if st.sidebar.button("🚪 Logout"):
    st.session_state.valid_user = False
    st.session_state.user = None
    st.session_state.image_captured = False
    st.session_state.img_str = None
    st.session_state.search_clicked = False

    st.rerun()

# 👉 STEP 1: Capture selfie
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

    # 🔄 Retake
    with col1:
        if st.button("🔄 Retake"):
            st.session_state.image_captured = False
            st.session_state.img_str = None
            st.session_state.search_clicked = False
            st.rerun()

    # 🔍 Search
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
                data = response.json()

                images = data.get("images", [])
                zip_url = data.get("zip_url")

                if not images:
                    st.warning("No matching photos found 😔")
                else:
                    st.success(f"Found {len(images)} matching photos 🎉")

                    # 👉 Grid layout
                    cols = st.columns(3)
                    for i, img_url in enumerate(images):
                        with cols[i % 3]:
                            st.image(img_url, use_container_width=True)

                    st.divider()

                    # 👉 Download section
                    if zip_url:
                        st.subheader("⬇️ Download All Photos")

                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.link_button("📦 Download ZIP",zip_url, use_container_width=True)
                        st.caption("Link valid for 1 hour")

            else:
                st.error(f"Error {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error("API request failed")
