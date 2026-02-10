from flask import Flask, Response, render_template_string
import requests
import cv2
import numpy as np
import re
import time
from threading import Lock

app = Flask(__name__)
streams = {}
stream_lock = Lock()

def parse_mjpeg(url):
    """Fetch and parse MJPEG stream into individual JPEGs"""
    try:
        r = requests.get(url, stream=True, timeout=10)
        if r.status_code == 200:
            content = r.raw.read(1024000)  # 1MB buffer
            jpg_start = content.find(b'\xff\xd8')
            jpg_end = content.find(b'\xff\xd9', jpg_start) + 2
            if jpg_start != -1 and jpg_end != -1:
                return content[jpg_start:jpg_end]
    except:
        pass
    return None

@app.route('/stream/<camera_id>')
def stream(camera_id):
    """Proxy MJPEG - clean stream for browsers"""
    def generate():
        url = streams.get(camera_id, "http://193.253.227.136:8081/mjpg/video.mjpg")
        while True:
            jpg = parse_mjpeg(url)
            if jpg:
                yield (b'--jpgboundary\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')
            time.sleep(0.1)
    
    return Response(generate(),
                   mimetype='multipart/x-mixed-replace; boundary=jpgboundary')

@app.route('/')
def index():
    """Insecam-style camera grid"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Insecam</title>
        <style>
            body { margin:0; font-family:Arial; background:#000; color:white; }
            .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(400px,1fr)); gap:10px; padding:20px; }
            .camera { background:#111; border-radius:10px; overflow:hidden; box-shadow:0 5px 15px rgba(0,0,0,0.5); }
            .camera img { width:100%; height:250px; object-fit:cover; }
            h1 { text-align:center; color:#ff4444; margin:20px; }
        </style>
    </head>
    <body>
        <h1>🔴 Live World Cameras ({{cameras|length}})</h1>
        <div class="grid">
            {% for id, name in cameras.items() %}
            <div class="camera">
                <img src="/stream/{{id}}" alt="{{name}}">
                <div style="padding:10px;">
                    <strong>{{name}}</strong>
                </div>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """, cameras={
        'cam1': 'Shodan Live 1',
        'cam2': 'Maharashtra Cam',
        # Add your cameras here
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
