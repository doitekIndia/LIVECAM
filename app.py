import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64
import time
import numpy as np
import json
import os

st.set_page_config(page_title="🔴 LiveCams", layout="wide", initial_sidebar_state="collapsed")

# Your beautiful CSS + AUTO-COLLAPSE SIDEBAR
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
/* AUTO-HIDE SIDEBAR WHEN NOT LOGGED IN */
[data-testid="collapsedControl"] {display: none !important;}
section[data-testid="stSidebar"] {width: 0px !important;}
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
        # Show login button to open sidebar
        with st.sidebar:
            st.markdown("### 🔐 **ADMIN LOGIN**")
            st.markdown("👆 **Click sidebar icon → Login**")
            username = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")
            
            if st.button("🚪 Login", use_container_width=True):
                if username == ADMIN_USER and password == ADMIN_PASS:
                    st.session_state.authenticated = True
                    st.success("✅ Admin access granted!")
                    st.rerun()
                else:
                    st.error("❌ Wrong credentials!")
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

# 🔐 ADMIN SECTION - Only visible after login
if check_admin_access():
    # SHOW FULL ADMIN CONTROLS IN SIDEBAR
    st.markdown("""
    <style>
    /* SHOW SIDEBAR WHEN LOGGED IN */
    [data-testid="collapsedControl"] {display: block !important;}
    section[data-testid="stSidebar"] {width: 280px !important;}
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### ✅ **ADMIN CONTROLS**")
        st.markdown(f"**📊 {len(cameras)} cameras loaded**")
        
        # ADD CAMERA FORM
        st.markdown("### ➕ **Add Camera**")
        new_name = st.text_input("🏷️ Name", value="🌍 New Camera")
        new_snapshot = st.text_input("📸 Snapshot URL", 
            value="http://IP:PORT/axis-cgi/jpg/image.cgi",
            help="Use /axis-cgi/jpg/image.cgi for thumbnails")
        new_stream = st.text_input("🔴 Stream URL", 
            value="http://IP:PORT/axis-cgi/mjpg/video.cgi", 
            help="Use /axis-cgi/mjpg/video.cgi or /mjpg/video.mjpg")
        
        col1, col2 = st.columns([3,1])
        with col1:
            if st.button("✅ ADD CAMERA", use_container_width=True):
                if all([new_name, new_snapshot, new_stream]):
                    new_cam = {"name": new_name, "snapshot": new_snapshot, "stream": new_stream}
                    st.session_state.cameras.append(new_cam)
                    save_cameras(st.session_state.cameras)
                    st.success("✅ Added!")
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.cameras = []
                save_cameras([])
                st.success("🗑️ Cleared!")
                st.rerun()
        
        st.markdown("---")
        
        # 🔥 GOOGLE DORK SEARCH BUTTON
        st.markdown("### 🔍 **Find New Cameras**")
        st.info("`inurl:\"/axis-cgi/mjpg/video.cgi\"` results")
        
        if st.button("🔍 **Add 5 Axis Cameras**", use_container_width=True):
            new_cameras = [
                {"name": "🌍 Europe 83.48", "snapshot": "http://83.48.75.113:8320/axis-cgi/jpg/image.cgi", "stream": "http://83.48.75.113:8320/axis-cgi/mjpg/video.cgi"},
                {"name": "🇳🇴 Tusten Norway", "snapshot": "http://live1.tusten.no:8080/axis-cgi/jpg/image.cgi", "stream": "http://live1.tusten.no:8080/axis-cgi/mjpg/video.cgi"},
                {"name": "🇩🇪 Anklam Germany", "snapshot": "http://webcam.anklam.de/axis-cgi/jpg/image.cgi", "stream": "http://webcam.anklam.de/axis-cgi/mjpg/video.cgi"},
                {"name": "🇺🇸 USA 50.245", "snapshot": "http://50.245.40.138:51695/axis-cgi/jpg/image.cgi", "stream": "http://50.245.40.138:51695/axis-cgi/mjpg/video.cgi"},
                {"name": "🌐 Dynamic DNS", "snapshot": "http://abcmaingate.dyndns.info:8083/axis-cgi/jpg/image.cgi", "stream": "http://abcmaingate.dyndns.info:8083/axis-cgi/mjpg/video.cgi"}
            ]
            added_count = 0
            for cam in new_cameras:
                if cam not in st.session_state.cameras:
                    st.session_state.cameras.append(cam)
                    added_count += 1
            save_cameras(st.session_state.cameras)
            st.success(f"✅ Added {added_count} cameras!")
            st.rerun()
        
        st.markdown("---")
        if st.button("🔓 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# Stats
st.markdown("---")
col1, col2 = st.columns(2)
col1.metric("📹 Total Cameras", len(cameras))
col2.caption("🔄 Auto-refreshing every 30 seconds...")
time.sleep(30)
st.rerun()
