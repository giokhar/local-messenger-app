import socket
from networking import helper

def create_socket(host, my_username, socketio, port=50010): # creates sockets if connection is possible in less than 0.2 seconds
	new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an empty socket
	new_socket.settimeout(0.2) # if connection takes more than 0.2 seconds do not connect
	new_socket.connect((host, port)) # connect using this type (host, port) tuple
	new_socket.sendall(my_username.encode('utf-8'));
	new_socket.settimeout(None)

	
	# your_username = new_socket.recv(1024).decode('utf-8');
	# data = {"username": your_username, "id": get_id(host)}
	# socketio.emit('user_joined', data)

	return new_socket # e.g. <socket>

def connected_sockets(my_username, socketio): # return a dictionary of connected hosts
	my_ip = helper.get_my_ip() # get my ip from the helper
	ip_list = helper.active_ip_adresses() # get a list of active ip addresses
	active_sockets = {} # dictionary to keep track of active sockets
	for host in ip_list: # iterate over active ips
		try:
			if host != my_ip: # create all sockets if not exist except my own
				new_socket = create_socket(host, my_username, socketio) # create socket if possible
				active_sockets[host] = (my_username, new_socket) # {'0.0.0.0':<socket>}
				print(active_sockets)
		except:
			pass # skip if cannot connect to the host
	return active_sockets # e.g. {'0.0.0.0':<socket1>, '0.0.0.1':<socket2>, ...}

def send_message(host, my_username, message, socketio): # sends message from this host to the other
	active_sockets = connected_sockets(my_username, socketio) # get all the active sockets again
	my_socket = active_sockets.get(host)[1] # get socket from sockets dict where key=host, value=(username, socket)
	my_socket.sendall(message.encode('utf-8')) # send message using this socket
	if message == "exit":
		my_socket.close()
	return message