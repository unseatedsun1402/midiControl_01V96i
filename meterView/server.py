from http.server import BaseHTTPRequestHandler, HTTPServer
import time,os, sys, deskConfig, Connection, threading, Parser
from flask import Flask, render_template, request, Blueprint,jsonify
from flask_socketio import SocketIO, emit

hostName = "localhost"
serverPort = 8080
global options
global PARSER
global input
global aux
global bus
global stereo
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
    app.config["HOST"] = "localhost"
    app.config["port"] = 5000

    app.register_blueprint(main)

    socketio.init_app(app)

    return app

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template('mixview.html',title='Personal Mixer',content = "Body goes here!", channels=inp)

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
    print(data)
    # pass

@socketio.on("options")
def handle_options():
    return aux

@main.route("/options")
async def handle_select():
    html = ""
    for each in aux:
        html += f'<option value="{each}">{aux[each].short}</option>'
    return {"html":html}



if __name__ == "__main__":
    app = create_app()
    conn = Connection.Connection()
    inp,bus,aux = deskConfig.setup(conn = conn, type = '01V96i')
    PARSER = Parser()
    socketio.run(app)

def start():
    app = create_app()
    socketio.run(app)