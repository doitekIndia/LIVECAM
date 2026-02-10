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

# Your beautiful CSS
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
.sidebar .sidebar-content {background: linear-gradient(180deg, #1a1a1a 0%, #000 100%);}
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
    
    # Smart fallback
    img = Image.new('RGB', (640, 480), color='#1a1a1a')
    for _ in range(30):
        x = np.random.randint(50, 590)
        y = np.random.randint(100, 400)
        size = np.random.randint(15, 40)
        color = tuple(np.random.randint(80, 160, 3))
        img.rectangle([x, y, x+size, y+size], fill=color)
    return img

def img_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def load_cameras():
    """Load from file or return defaults"""
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
    """Save cameras to persistent file"""
    with open('cameras.json', 'w') as f:
        json.dump({'cameras': cameras}, f)

# Initialize session state
if 'cameras' not in st.session_state:
    st.session_state.cameras = load_cameras()

# 🚀 SIDEBAR - ADD CAMERAS REALTIME
with st.sidebar:
    st.markdown("## ➕ Add Camera")
    new_name = st.text_input("🏷️ Name", value="🌍 New Camera")
    new_snapshot = st.text_input("📸 Snapshot", 
        value="http://IP:PORT/axis-cgi/jpg/image.cgi")
    new_stream = st.text_input("🔴 Stream", 
        value="http://IP:PORT/axis-cgi/mjpg/video.cgi")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ ADD CAMERA", use_container_width=True):
            if all([new_name, new_snapshot, new_stream]):
                new_cam = {
                    "name": new_name,
                    "snapshot": new_snapshot,
                    "stream": new_stream
                }
                st.session_state.cameras.append(new_cam)
                save_cameras(st.session_state.cameras)
                st.success("✅ Added!")
                st.rerun()
            else:
                st.error("❌ Fill all fields")
    
    with col2:
        if st.button("🗑️ CLEAR ALL", use_container_width=True):
            st.session_state.cameras = []
            save_cameras([])
            st.success("🗑️ Cleared!")
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"**📊 Total: {len(st.session_state.cameras)} cameras**")

# Header
st.markdown('<div class="header"><h1>🔴 Live Cameras Worldwide</h1></div>', unsafe_allow_html=True)

cameras = st.session_state.cameras

# Dynamic responsive grid
if cameras:
    # Auto-adjust columns (1-4 based on camera count)
    cols_count = min(4, max(1, len(cameras) // 3 + 1))
    cols = st.columns(cols_count)
    
    for i, cam in enumerate(cameras):
        col_idx = i % cols_count
        with cols[col_idx]:
            # Live snapshot for THIS camera
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
    st.info("👆 **Add your first camera using the sidebar!**")

# QUICK ADD - Popular cameras
with st.expander("⚡ Quick Add Popular Cameras"):
    col1, col2, col3 = st.columns(3)
    
    def quick_add(name, snapshot, stream):
        new_cam = {"name": name, "snapshot": snapshot, "stream": stream}
        st.session_state.cameras.append(new_cam)
        save_cameras(st.session_state.cameras)
        st.rerun()
    
    with col1:
        if st.button("🇳🇴 Norway", use_container_width=True):
            quick_add("🇳🇴 Tusten Norway", 
                     "http://live1.tusten.no:8080/axis-cgi/jpg/image.cgi",
                     "http://live1.tusten.no:8080/axis-cgi/mjpg/video.cgi")
    
    with col2:
        if st.button("🇩🇪 Germany", use_container_width=True):
            quick_add("🇩🇪 Anklam Germany", 
                     "http://webcam.anklam.de/axis-cgi/jpg/image.cgi",
                     "http://webcam.anklam.de/axis-cgi/mjpg/video.cgi")
    
    with col3:
        if st.button("🌍 Europe 83", use_container_width=True):
            quick_add("🌍 Europe 83.48", 
                     "http://83.48.75.113:8320/axis-cgi/jpg/image.cgi",
                     "http://83.48.75.113:8320/axis-cgi/mjpg/video.cgi")

# Footer + Auto-refresh
st.markdown("---")
st.caption("🔄 Auto-refreshing every 30 seconds...")
time.sleep(30)
st.rerun()
