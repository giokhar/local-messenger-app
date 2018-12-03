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
	ip = "192.168.1.1" # take the last digit of IP address as an id, e.g id=1
	socketio.emit('message_received', {"id":request.args['id'],"text":request.args['text']})
	return "MESSAGE WAS SENT FROM "+ request.args['id']

@app.route('/friend')
def friend():
	# send user icon if you have enough time
	# When sending username check if that username already exists
	ip = "192.168.1.1" # take the last digit of IP address as an id
	data = {"username": request.args['username'], "id": request.args['id']}
	socketio.emit('user_joined', data)
	return "NEW USER HAS JOINED THE NETWORK"

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('message_sent', json)

if __name__ == '__main__':
    socketio.run(app, debug=True)