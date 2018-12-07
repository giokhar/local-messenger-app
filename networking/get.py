import socket, threading
from networking import settings
from networking.helper import get_my_ip, get_id
from networking.post import create_socket, send_message
import json

def handle_new_client(socket, host, socketio):

	data = socket.recv(1024)

	json_data = json.loads(data.decode('utf-8')) # {"host", "username", "message_type", "message"}
	print("Recieved: ",json_data)

	id = get_id(host)
	username = json_data['username']
	message_type = int(json_data['message_type'])
	message = json_data['message']

	if message_type == 0:#Connection Request with name
		my_data = {"id": id, "username": username}
		socketio.emit('user_joined', my_data)
		send_message(host, 1, settings.my_username)

	elif message_type == 1:#I don't need name sent back
		my_data = {"id": id, "username": username}
		socketio.emit('second_user_joined', my_data)

	elif message_type == 2:#Disconnect Request
		my_data = {"id":id}
		socketio.emit("user_left", my_data)

	elif message_type == 3:#Regular message
		my_data = {"id": id, "user": username, "text": message}
		socketio.emit('message_received', my_data)
			
	socket.close()

def listener(socketio, port=50011):
	host = get_my_ip() # method is imported from networking.helper
	print("listening on", host, "port", port)
	 
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((host, port))
	server_socket.listen(6)

	while True:
		new_socket, addr = server_socket.accept()
		print ("Connection from", addr)
		#A thread shuts down itself after handling new client.
		new_client_thread = threading.Thread(target = handle_new_client, args = (new_socket, addr[0], socketio))
		new_client_thread.start()
	server_socket.close()