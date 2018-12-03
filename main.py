from flask import Flask, request, render_template
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'NO_SECRET_KEY'
socketio = SocketIO(app)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/chat')
def chat():
	username = request.args['username']
	return render_template('chat.html', username=username)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)