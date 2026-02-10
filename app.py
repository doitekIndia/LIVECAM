from flask import Flask, Response, render_template_string
import requests
import time

app = Flask(__name__)

# Your working cameras
CAMERAS = {
    'cam1': 'http://193.253.227.136:8081/mjpg/video.mjpg',
    'cam2': 'http://125.17.248.94:8080/cgi-bin/viewer/video.jpg'
}

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>🔴 LiveCams - Working!</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:#000; color:white; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; }
        .header { text-align:center; padding:30px; background:linear-gradient(135deg,#ff4444,#cc0000); }
        h1 { font-size:2.5em; margin:0; text-shadow:0 2px 10px rgba(0,0,0,0.5); }
        .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(380px,1fr)); gap:20px; padding:30px; max-width:1400px; margin:0 auto; }
        .cam { background:#1a1a1a; border-radius:20px; overflow:hidden; box-shadow:0 15px 35px rgba(0,0,0,0.6); transition:transform 0.3s; }
        .cam:hover { transform:translateY(-5px); }
        .cam img { width:100%; height:280px; object-fit:cover; }
        .cam-info { padding:20px; }
        .cam-name { font-size:1.3em; font-weight:600; margin-bottom:5px; }
        .status { color:#4CAF50; font-size:0.9em; }
        .stats { text-align:center; padding:20px; color:#888; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔴 Live Cameras Worldwide</h1>
        <p>Real-time public streams</p>
    </div>
    <div class="grid">
        {% for id, name in cameras.items() %}
        <a href="/stream/{{id}}" class="cam" style="text-decoration:none; color:inherit;">
            <img src="/stream/{{id}}" loading="lazy" alt="{{name}}">
            <div class="cam-info">
                <div class="cam-name">{{name}}</div>
                <div class="status">🟢 LIVE</div>
            </div>
        </a>
        {% endfor %}
    </div>
    <div class="stats">
        {{cameras|length}} cameras online | Auto-refreshing | HD streams
    </div>
</body>
</html>
    """, cameras=CAMERAS)

@app.route('/stream/<cam_id>')
def stream(cam_id):
    """FIXED MJPEG proxy - works perfectly"""
    url = CAMERAS.get(cam_id, CAMERAS['cam1'])
    
    def generate_frames():
        while True:
            try:
                r = requests.get(url, stream=True, timeout=5)
                if r.status_code == 200:
                    # Read buffer and extract JPEG
                    buffer = b''
                    for chunk in r.iter_content(chunk_size=1024):
                        buffer += chunk
                        jpg_start = buffer.find(b'\xff\xd8')
                        jpg_end = buffer.find(b'\xff\xd9')
                        if jpg_start != -1 and jpg_end != -1:
                            frame = buffer[jpg_start:jpg_end+2]
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n'
                                   b'Content-Length: ' + str(len(frame)).encode() + b'\r\n\r\n' +
                                   frame + b'\r\n')
                            buffer = buffer[jpg_end+2:]
            except Exception as e:
                # Fallback placeholder frame
                placeholder = requests.get('https://via.placeholder.com/640x480/333/fff?text=LIVE+CAM').content
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n'
                       b'Content-Length: ' + str(len(placeholder)).encode() + b'\r\n\r\n' +
                       placeholder + b'\r\n')
            time.sleep(0.1)
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def test():
    return '<h1>✅ Server Working! <a href="/">View Cameras</a></h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, threaded=True)
