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


# CUSTOM ROUTES TO TEST FRONT-END WITHOUT BACK-END

@app.route('/message')
def message():
	socketio.emit('my response', {"from":request.args['from'],"text":request.args['message']}, callback=messageReceived)
	return "MESSAGE WAS SENT FROM "+ request.args['from']

@app.route('/friend')
def friend():
	# When sending username check if that username already exists
	ip = "192.168.1.1" # take the last digit of IP address as an id
	data = {"username": request.args['username'], "id": request.args['id']}
	socketio.emit('user_joined', data)
	return "NEW USER HAS JOINED THE NETWORK"

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json)

if __name__ == '__main__':
    socketio.run(app, debug=True)