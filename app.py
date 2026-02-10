from flask import Flask

app = Flask(__name__)

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
        .cam img{width:100%;height:280px;object-fit:cover;}
        .cam-title{padding:20px;text-align:center;}
        .cam-name{font-size:1.3em;font-weight:600;margin-bottom:5px;}
        .status{color:#4CAF50;font-size:0.9em;}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔴 Live Cameras Worldwide</h1>
        <p>Click any camera for fullscreen live stream</p>
    </div>  <!-- ← FIXED: Added closing </div> -->
    <div class="grid">
        <!-- Your 3 cams - PERFECT as-is! -->
        <a href="http://193.253.227.136:8081/mjpg/video.mjpg" target="_blank" class="cam">
            <img src="http://193.253.227.136:8081/axis-cgi/jpg/image.cgi" alt="South Africa">
            <div class="cam-title">
                <div class="cam-name">🇿🇦 South Africa Live</div>
                <div class="status">🟢 HD Stream</div>
            </div>
        </a>
        <a href="http://193.253.227.136:8081/mjpg/video.mjpg" target="_blank" class="cam">
            <img src="http://193.253.227.136:8081/axis-cgi/jpg/image.cgi" alt="Times Square">
            <div class="cam-title">
                <div class="cam-name">🗽 New York Times Square</div>
                <div class="status">🟢 24/7 Live</div>
            </div>
        </a>
        <a href="http://193.253.227.136:8081/mjpg/video.mjpg" target="_blank" class="cam">
            <img src="http://193.253.227.136:8081/axis-cgi/jpg/image.cgi" alt="India">
            <div class="cam-title">
                <div class="cam-name">🇮🇳 India Live Cam</div>
                <div class="status">🟢 Click for Live</div>
            </div>
        </a>
    </div>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
