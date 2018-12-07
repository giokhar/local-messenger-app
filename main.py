from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO
from networking.post import send_message, broadcast
from networking.get import listener
from networking.helper import get_ip_no_id
from networking import settings
import threading

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'NO_SECRET_KEY'
socketio = SocketIO(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/chat', methods=['GET', "POST"])
def chat():
	settings.my_username = request.form['username'] # get the username from the POST form
	while settings.my_username:
		broadcast(0) # connect to everyone
		break
	return render_template('chat.html', username=settings.my_username)

@app.route('/logout')
def logout():
	# send the server that you left and redirect to the url
	broadcast(2) # disconnect from everyone
	return redirect(url_for('login'))

@socketio.on('my_event') # invoked when user sends a message
def handle_my_custom_event(data, methods=['GET', 'POST']):
	print(str(data)) # json object containing receiver's id (or ip) and the text
	socketio.emit('message_sent', data)
	host = get_ip_no_id() + "." + str(data['id']) # get hosts ip from id coming from the browser
	message = data['text'] # get the message from the browser
	send_message(host, 3, message) # networking.send_message

if __name__ == '__main__':
	settings.init() #Initializes the global variable
	run_app_thread = threading.Thread(target = socketio.run, args = (app,))
	run_get_thread = threading.Thread(target = listener, args = (socketio,))
	run_app_thread.start()
	run_get_thread.start()