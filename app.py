from flask import Flask, render_template_string

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
        body {margin:0; background:#000; color:#fff; font-family:Arial;}
        .grid {display:grid; grid-template-columns:repeat(auto-fill,minmax(400px,1fr)); gap:20px; padding:30px;}
        .cam {border-radius:15px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.5);}
        .cam img {width:100%; height:300px; object-fit:cover;}
        h1 {text-align:center; color:#ff4444; padding:30px;}
    </style>
</head>
<body>
    <h1>🔴 Live Cameras (Click to View)</h1>
    <div class="grid">
        <a href="http://193.253.227.136:8081/mjpg/video.mjpg" target="_blank" class="cam" style="text-decoration:none; color:inherit;">
            <img src="http://193.253.227.136:8081/mjpg/video.mjpg?t=1" alt="Live Cam 1" onerror="this.src='https://via.placeholder.com/400x300/ff4444/fff?text=LIVE+CAM'">
            <div style="padding:20px; text-align:center;"><strong>📹 Shodan Live Cam</strong></div>
        </a>
        <a href="http://125.17.248.94:8080/cgi-bin/viewer/video.jpg" target="_blank" class="cam" style="text-decoration:none; color:inherit;">
            <img src="http://125.17.248.94:8080/cgi-bin/viewer/video.jpg?t=2" alt="Live Cam 2" onerror="this.src='https://via.placeholder.com/400x300/4444ff/fff?text=LIVE+CAM'">
            <div style="padding:20px; text-align:center;"><strong>📹 Maharashtra Cam</strong></div>
        </a>
    </div>
</body>
</html>
    '''

@app.route('/test')
def test():
    return '<h1 style="color:green;">✅ SERVER WORKING! <a href="/">View Cameras</a></h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
