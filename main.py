from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO
from networking.post import send_message,connected_sockets
from networking.get import listener
from networking.helper import get_ip_no_id, get_id, active_ip_adresses
import threading

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'NO_SECRET_KEY'
socketio = SocketIO(app)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/chat', methods=['GET', "POST"])
def chat():
	my_username = request.form['username'] # get the username from the POST form
	sockets = connected_sockets(my_username, socketio) # print connected_sockets and pass username to all the devices
	# for ip, user_socket in sockets.items():
	# 	data = {"username": user_socket[0], "id": get_id(ip)}
	# 	socketio.emit('user_joined', data)
	return render_template('chat.html', username=username)

@app.route('/logout')
def logout():
	# send the server that you left and redirect to the url
	return redirect(url_for('login'))


# CUSTOM ROUTES TO TEST FRONT-END WITHOUT BACK-END

@app.route('/message')
def message():
	ip = "192.168.1.1" # take the last digit of IP address as an id, e.g id=1
	data = {"id":request.args['id'],"text":request.args['text']}
	socketio.emit('message_received', data)
	return "MESSAGE WAS SENT FROM "+ request.args['id']

@app.route('/join')
def join():
	# send user icon if you have enough time
	# When sending username check if that username already exists
	ip = "192.168.1.1" # take the last digit of IP address as an id
	data = {"username": request.args['username'], "id": request.args['id']}
	socketio.emit('user_joined', data)
	return "NEW USER HAS JOINED THE NETWORK"

@app.route('/rejoin')
def rejoin():
	data = {"id": request.args['id']}
	socketio.emit('user_rejoined', data)
	return "USER Rejoined"

@app.route('/leave')
def leave():
	data = {"id": request.args['id']}
	socketio.emit('user_left', data)
	return "USER LEFT"

@socketio.on('my_event') # invoked when user sends a message
def handle_my_custom_event(data, methods=['GET', 'POST']):
    print(str(data)) # json object containing receiver's id (or ip) and the text
    socketio.emit('message_sent', data)
    host = get_ip_no_id() + "." + str(data['id']) # get hosts ip from id coming from the browser
    username = data['user'] # get my username from front-end
    message = data['text'] # get the message from the browser
    send_message(host, username, message) # networking.send_message

@socketio.on('')
def set_users(users): # dictionary of "username": "id"
	for username, id in users.items():
		data = {"username":username, "id":id}
		socketio.emit('user_joined', data)

if __name__ == '__main__':
	run_app_thread = threading.Thread(target = socketio.run, args = (app,))
	run_get_thread = threading.Thread(target = listener, args = (socketio,))
	run_app_thread.start()
	run_get_thread.start()