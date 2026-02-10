import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64
import time
import numpy as np
import json
import os

st.set_page_config(page_title="🔴 LiveCams", layout="wide")

# Your beautiful CSS + HIDE ADD SECTION BY DEFAULT
st.markdown("""
<style>
.header{text-align:center;padding:40px;background:linear-gradient(135deg,#ff4444,#cc0000);border-radius:20px;margin-bottom:30px;}
h1{font-size:3em;color:white;text-shadow:0 2px 10px rgba(0,0,0,0.5);}
.cam-container{background:#1a1a1a;border-radius:20px;overflow:hidden;box-shadow:0 15px 35px rgba(0,0,0,0.6);text-decoration:none;color:white;display:block;transition:transform 0.3s;}
.cam-container:hover{transform:translateY(-5px);}
.cam-img{width:100%;height:280px;object-fit:cover;}
.cam-title{padding:20px;text-align:center;}
.cam-name{font-size:1.3em;font-weight:600;}
.status{color:#4CAF50;}
#admin-section {display: none;}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def get_live_snapshot(snapshot_url):
    """Get snapshot from specific camera"""
    try:
        resp = requests.get(snapshot_url, timeout=8)
        if resp.status_code == 200:
            img = Image.open(BytesIO(resp.content))
            img = img.resize((640, 480))
            return img
    except:
        pass
    img = Image.new('RGB', (640, 480), color='#1a1a1a')
    return img

def img_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def load_cameras():
    """Load cameras from file or defaults"""
    try:
        if os.path.exists('cameras.json'):
            with open('cameras.json', 'r') as f:
                return json.load(f).get('cameras', [])
    except:
        pass
    return [
        {
            "name": "🇿🇦 South Africa Warehouse",
            "snapshot": "http://193.253.227.136:8081/axis-cgi/jpg/image.cgi",
            "stream": "http://193.253.227.136:8081/mjpg/video.mjpg"
        }
    ]

def save_cameras(cameras):
    """Save cameras to file"""
    with open('cameras.json', 'w') as f:
        json.dump({'cameras': cameras}, f)

# 🔐 PASSWORD CHECK using Streamlit Secrets
def check_admin_access():
    ADMIN_USER = st.secrets.get("ADMIN_USER", "admin")
    ADMIN_PASS = st.secrets.get("ADMIN_PASS", "password123")
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Show login only if not authenticated
    if not st.session_state.authenticated:
        with st.sidebar:
            st.markdown("### 🔐 **ADMIN LOGIN**")
            username = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")
            
            if st.button("🚪 Login", use_container_width=True):
                if username == ADMIN_USER and password == ADMIN_PASS:
                    st.session_state.authenticated = True
                    st.success("✅ Admin access granted!")
                    st.rerun()
                else:
                    st.error("❌ Wrong credentials!")
            st.markdown("---")
        return False
    
    return True

# Initialize cameras
if 'cameras' not in st.session_state:
    st.session_state.cameras = load_cameras()

# Header
st.markdown('<div class="header"><h1>🔴 Live Cameras Worldwide</h1><p>Click any camera for fullscreen live stream</p></div>', unsafe_allow_html=True)

cameras = st.session_state.cameras

# Show cameras grid
if cameras:
    cols_count = min(4, max(1, len(cameras) // 3 + 1))
    cols = st.columns(cols_count)
    
    for i, cam in enumerate(cameras):
        col_idx = i % cols_count
        with cols[col_idx]:
            img = get_live_snapshot(cam["snapshot"])
            img_b64 = img_to_base64(img)
            st.markdown(f"""
            <a href="{cam['stream']}" target="_blank" class="cam-container" style="text-decoration:none;">
                <img src="data:image/jpeg;base64,{img_b64}" class="cam-img">
                <div class="cam-title">
                    <div class="cam-name">{cam['name']}</div>
                    <div class="status">🟢 LIVE</div>
                </div>
            </a>
            """, unsafe_allow_html=True)
else:
    st.info("📹 No cameras available")

# 🔐 ADMIN SECTION - HIDDEN BY DEFAULT
if check_admin_access():
    # Show admin controls in sidebar
    with st.sidebar:
        st.markdown("### ✅ **ADMIN CONTROLS**")
        st.markdown(f"**📊 {len(cameras)} cameras loaded**")
        
        # ADD CAMERA FORM
        st.markdown("### ➕ **Add Camera**")
        new_name = st.text_input("🏷️ Name")
        new_snapshot = st.text_input("📸 Snapshot URL")
        new_stream = st.text_input("🔴 Stream URL")
        
        if st.button("✅ ADD CAMERA", use_container_width=True):
            if all([new_name, new_snapshot, new_stream]):
                new_cam = {"name": new_name, "snapshot": new_snapshot, "stream": new_stream}
                st.session_state.cameras.append(new_cam)
                save_cameras(st.session_state.cameras)
                st.success("✅ Added!")
                st.rerun()
        
        # Quick add buttons
        if st.button("🇳🇴 Add Norway", use_container_width=True):
            st.session_state.cameras.append({
                "name": "🇳🇴 Tusten Norway", 
                "snapshot": "http://live1.tusten.no:8080/axis-cgi/jpg/image.cgi",
                "stream": "http://live1.tusten.no:8080/axis-cgi/mjpg/video.cgi"
            })
            save_cameras(st.session_state.cameras)
            st.rerun()
        
        st.markdown("---")
        if st.button("🔓 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# Quick stats
st.markdown("---")
col1, col2 = st.columns(2)
col1.metric("📹 Total Cameras", len(cameras))
col2.caption("🔄 Auto-refreshing every 30 seconds...")
time.sleep(30)
st.rerun()
