import socket, threading
from networking import settings
from networking.helper import get_my_ip, get_id
from networking.post import create_socket, send_message

def handle_new_client(socket, host, current_sockets, socketio):
	while True:
		data = socket.recv(1024)

		if not data: break
		dec_data = data.decode('utf-8')
		print("Recieved: "+ dec_data)

		message_type = int(dec_data[0])
		id = get_id(host)

		if message_type == 0:#Connection Request with name

			username = dec_data[1:] #if message type is 0, then the message contains only the username
			my_data = {"id": id, "user": username, "text": dec_data[1:]}
			socketio.emit('user_joined', my_data)

			send_socket = create_socket(host)
			current_sockets[host] = [username, send_socket]

			send_message(host, 1, settings.my_username, current_sockets)

		elif message_type == 1:#I don't need name back
			username = dec_data[1:]
			# settings.current_sockets[host][0] = username
			current_sockets[host] = [username, current_sockets[host][1]]
			my_data = {"id": id, "user": username, "text": dec_data[1:]}
			socketio.emit('user_joined', my_data)

		elif message_type == 2:#Disconnect Request
			#need to remove host from the routing table
			del current_sockets[host]
			break

		elif message_type == 3:#Regular message

			message = dec_data[1:]
			username = current_sockets[host][0]
			my_data = {"id": id, "user": username, "text": dec_data[1:]}
			socketio.emit('message_received', my_data)
			
	socket.close()

def listener(socketio, current_sockets, port=50011):
	host = get_my_ip() # method is imported from networking.helper
	print("listening on", host, "port", port)
	 
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((host, port))
	server_socket.listen(6)

	while True:
		new_socket, addr = server_socket.accept()
		print ("Connection from", addr)
		#A thread shuts down itself after handling new client.
		new_client_thread = threading.Thread(target = handle_new_client, args = (new_socket, addr[0], current_sockets, socketio))
		new_client_thread.start()
	server_socket.close()