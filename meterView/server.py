from http.server import BaseHTTPRequestHandler, HTTPServer
import time,os, sys, inputChannel, stereoBus, Parser, AUXchannel, BUSchannel
from flask import Flask, render_template, request, Blueprint
from flask_socketio import SocketIO, emit

hostName = "localhost"
serverPort = 8080
global options
socketio = SocketIO()

channels = [
    {
        "id":0,
        "name":"ch1",
        "level":55
    },
    {
        "id":1,
        "name":"ch2",
        "level":75
    },
    {
        "id":2,
        "name":"ch3"
    },
    {
        "id":3,
        "name":"ch4"
    }
    ]

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "secret"

    app.register_blueprint(main)

    socketio.init_app(app)

    return app

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template('mixview.html',title='Personal Mixer',content = "Body goes here!", channels=channels)

# @app.route('/',methods=['GET','POST'])
# def hello():
    # return render_template('mixview.html',title='Personal Mixer',content = "Body goes here!", channels=channels)


# @app.route('/about')
# def description():
# return "<body><p>\
# this is a desription</p></body>"


#@app.errorhandler(404)
#def not_found(error):
#    return render_template('error.html'), 404

@socketio.on("connect")
def handle_connect():
    print('connected')

@socketio.on("faderchange")
def handleChange(data):
    # print(f"{data['channel']}: {data['value']}")
    pass


if __name__ == "__main__":
    app = create_app()
    socketio.run(app)

def start():
    app = create_app
    socketio.run(app)