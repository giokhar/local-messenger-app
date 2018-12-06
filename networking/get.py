import socket, threading
from networking import settings
from networking.helper import get_my_ip, get_id

def handle_new_client(socket, addr, socketio):
	while True:
		data = socket.recv(1024)
		if not data: break
		dec_data = data.decode('utf-8')
		print("Recieved: "+ dec_data)
		message_type = int(dec_data[0])

		id = get_id(addr[0])
		if message_type == 0:#Connection Request
			print(dec_data)
			username = dec_data[1:] #if message type is 0, then the message contains only the username
			my_data = {"id": id, "user": username, "text": dec_data}
			socketio.emit('user_joined', my_data)
			socket.sendall(("0"+ settings.my_username).encode('utf-8'))
			settings.current_sockets[addr[0]] = (username, socket)

		elif message_type == 1:#Disconnect Request
			#need to remove host from the routing table
			del settings.current_sockets[host]
			break

		elif message_type == 2:#Regular message

			message = dec_data[1:]
			username = settings.current_sockets[host][0] #BUG HERE! SHOULD BE USER FOR [0]
			my_data = {"id": id, "user": username, "text": dec_data}
			socketio.emit('message_received', my_data)
			
	socket.close()

def listener(socketio, port=50010):
	host = get_my_ip() # method is imported from networking.helper
	print("listening on", host, "port", port)
	 
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((host, port))
	server_socket.listen(6)

	while True:
		new_socket, addr = server_socket.accept()
		print ("Connection from", addr)
		#A thread shuts down itself after handling new client.
		new_client_thread = threading.Thread(target = handle_new_client, args = (new_socket, addr,socketio))
		new_client_thread.start()
	server_socket.close()