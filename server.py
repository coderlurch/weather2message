import socket
from flask import Flask

app = Flask(__name__)

@app.route('/<name>')
def post_weather_message(name):
    return "weather info"

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_url(name):
        return f"http://{get_ip()}:5000/{name}"

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)