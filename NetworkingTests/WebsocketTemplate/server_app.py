from threading import Lock

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

"""

Author: Joshua Ashley

Description: This is a basic flask web socket for testing and basic server/client crosstalk. This will go on the robot
to be able to receive controller input from a web client and produce sensor output.

Changelog:

1-30-2019 - Josh A - Created.

"""
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('server_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('keypress', namespace='/test')
def control(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    if message['data'] == 'up':
        emit('server_response', {'data': message['data'], 'count': session['receive_count']})
    elif message['data'] == 'down':
        emit('server_response', {'data': message['data'], 'count': session['receive'
                                                                           '_count']})


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('server_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('server_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
