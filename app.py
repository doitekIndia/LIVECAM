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
        body {margin:0; background:#000; color:#fff; font-family:Arial;}
        .grid {display:grid; grid-template-columns:repeat(auto-fill,minmax(400px,1fr)); gap:20px; padding:30px;}
        .cam {border-radius:15px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.5);}
        .cam img {width:100%; height:300px; object-fit:cover;}
        h1 {text-align:center; color:#ff4444; padding:30px;}
        .loading {background:#333; display:flex; align-items:center; justify-content:center; color:#fff; height:300px;}
    </style>
</head>
<body>
    <h1>🔴 Live Cameras Worldwide</h1>
    <div class="grid">
        <a href="http://193.253.227.136:8081/mjpg/video.mjpg" target="_blank" class="cam" style="text-decoration:none; color:inherit;">
            <img src="http://193.253.227.136:8081/mjpg/video.mjpg?t=1" 
                 onerror="this.outerHTML='<div class=\\'loading\\'>📡 LOADING LIVE STREAM...</div>'"
                 alt="Shodan Live Cam">
            <div style="padding:20px; text-align:center;"><strong>🌍 Shodan Live Cam</strong></div>
        </a>
        <a href="http://125.17.248.94:8080/cgi-bin/viewer/video.jpg" target="_blank" class="cam" style="text-decoration:none; color:inherit;">
            <img src="http://125.17.248.94:8080/cgi-bin/viewer/video.jpg?t=2" 
                 onerror="this.outerHTML='<div class=\\'loading\\'>📡 LOADING LIVE STREAM...</div>'"
                 alt="Maharashtra Cam">
            <div style="padding:20px; text-align:center;"><strong>🇮🇳 Maharashtra Cam</strong></div>
        </a>
    </div>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
