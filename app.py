import streamlit as st
import requests
from io import BytesIO
import time

st.set_page_config(
    page_title="🔴 LiveCams Worldwide",
    page_icon="📹",
    layout="wide"
)

# Custom CSS (your beautiful design)
st.markdown("""
    <style>
    .header {text-align:center;padding:40px;background:linear-gradient(135deg,#ff4444,#cc0000);border-radius:20px;margin-bottom:30px}
    h1 {font-size:3em;color:white;text-shadow:0 2px 10px rgba(0,0,0,0.5);margin:0;}
    .cam-container {background:#1a1a1a;border-radius:20px;overflow:hidden;box-shadow:0 15px 35px rgba(0,0,0,0.6);text-decoration:none;color:white;display:block;transition:transform 0.3s;}
    .cam-container:hover {transform:translateY(-5px);}
    .cam-img {width:100%;height:280px;object-fit:cover;}
    .cam-title {padding:20px;text-align:center;}
    .cam-name {font-size:1.3em;font-weight:600;margin-bottom:5px;}
    .status {color:#4CAF50;font-size:0.9em;}
    </style>
""", unsafe_allow_html=True)

def get_snapshot(cam_url):
    """Proxy snapshot from Axis camera"""
    try:
        resp = requests.get(cam_url, timeout=10)
        if resp.status_code == 200:
            return resp.content
    except:
        pass
    # Transparent fallback
    return b'R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='

# Cameras config
cameras = {
    "🇿🇦 South Africa": "http://193.253.227.136:8081/axis-cgi/jpg/image.cgi",
    "🗽 Times Square": "http://193.253.227.136:8081/axis-cgi/jpg/image.cgi", 
    "🇮🇳 India Cam": "http://193.253.227.136:8081/axis-cgi/jpg/image.cgi"
}

# Header
st.markdown("""
    <div class="header">
        <h1>🔴 Live Cameras Worldwide</h1>
        <p>Click any camera for fullscreen live stream</p>
    </div>
""", unsafe_allow_html=True)

# Camera grid (3 columns)
cols = st.columns(3)
for i, (name, snap_url) in enumerate(cameras.items()):
    with cols[i]:
        live_url = snap_url.replace("axis-cgi/jpg/image.cgi", "mjpg/video.mjpg")
        
        # Timestamp for auto-refresh
        timestamp = int(time.time())
        
        st.markdown(f"""
            <a href="{live_url}" target="_blank" class="cam-container">
                <img src="{snap_url}?t={timestamp}" class="cam-img" alt="{name}">
                <div class="cam-title">
                    <div class="cam-name">{name}</div>
                    <div class="status">🟢 HD Stream</div>
                </div>
            </a>
        """, unsafe_allow_html=True)

# Auto-refresh
st.markdown("---")
st.caption("🔄 Auto-refreshing every 30 seconds...")
time.sleep(30)
st.rerun()
