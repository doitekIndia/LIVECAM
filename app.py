from flask import Flask, Response
import requests
import time

app = Flask(__name__)

# Proxy ALL camera snapshots through YOUR Flask server
@app.route('/snap/<int:cam_id>')
def snapshot(cam_id):
    """Serve live snapshot from Axis camera via your Flask proxy"""
    cam_url = 'http://193.253.227.136:8081/axis-cgi/jpg/image.cgi'
    try:
        resp = requests.get(cam_url, timeout=5)
        if resp.status_code == 200:
            return Response(resp.content, mimetype='image/jpeg')
    except:
        pass
    # Fallback: transparent pixel
    return Response(b'R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=', mimetype='image/gif')

@app.route('/live/<int:cam_id>')
def live(cam_id):
    """Proxy the LIVE MJPEG stream too (for fullscreen)"""
    resp = requests.get('http://193.253.227.136:8081/mjpg/video.mjpg', stream=True, timeout=10)
    def generate():
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                yield chunk
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>🔴 LiveCams</title>
    <meta name="viewport" content="width=device-width">
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{background:#000;color:#fff;font-family:Arial;}
        .header{text-align:center;padding:40px;background:linear-gradient(135deg,#ff4444,#cc0000);}
        h1{font-size:2.5em;margin:0;text-shadow:0 2px 10px rgba(0,0,0,0.5);}
        .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:20px;padding:30px;max-width:1400px;margin:0 auto;}
        .cam{background:#1a1a1a;border-radius:20px;overflow:hidden;box-shadow:0 15px 35px rgba(0,0,0,0.6);text-decoration:none;color:inherit;display:block;transition:transform 0.3s;}
        .cam:hover{transform:translateY(-5px);}
        .cam img{width:100%;height:280px;object-fit:cover;object-position:center;}
        .cam-title{padding:20px;text-align:center;}
        .cam-name{font-size:1.3em;font-weight:600;margin-bottom:5px;}
        .status{color:#4CAF50;font-size:0.9em;}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔴 Live Cameras Worldwide</h1>
        <p>Click any camera for fullscreen live stream</p>
    </div>
    <div class="grid">
        <!-- CAMERA 1: South Africa -->
        <a href="/live/1" target="_blank" class="cam">
            <img src="/snap/1?t=<%:int(time.time())%>" alt="South Africa" loading="lazy">
            <div class="cam-title">
                <div class="cam-name">🇿🇦 South Africa Live</div>
                <div class="status">🟢 HD Stream</div>
            </div>
        </a>
        
        <!-- CAMERA 2: Times Square (same feed for demo) -->
        <a href="/live/2" target="_blank" class="cam">
            <img src="/snap/2?t=<%:int(time.time())%>" alt="Times Square" loading="lazy">
            <div class="cam-title">
                <div class="cam-name">🗽 New York Times Square</div>
                <div class="status">🟢 24/7 Live</div>
            </div>
        </a>
        
        <!-- CAMERA 3: India Cam -->
        <a href="/live/3" target="_blank" class="cam">
            <img src="/snap/3?t=<%:int(time.time())%>" alt="India" loading="lazy">
            <div class="cam-title">
                <div class="cam-name">🇮🇳 India Live Cam</div>
                <div class="status">🟢 Click for Live</div>
            </div>
        </a>
    </div>
    <script>
        // Auto-refresh thumbnails every 30 seconds
        setInterval(()=>{
            document.querySelectorAll('img').forEach((img,i)=>{
                img.src = img.src.split('?')[0] + '?t=' + Date.now();
            });
        }, 30000);
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
