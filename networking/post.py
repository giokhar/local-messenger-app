import socket
from networking import settings
from networking import helper

def create_socket(host, port=50010): # creates sockets if connection is possible in less than 0.2 seconds
	new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an empty socket
	new_socket.settimeout(0.5) # if connection takes more than 0.2 seconds do not connect
	new_socket.connect((host, port)) # connect using this type (host, port) tuple
	new_socket.settimeout(None)
	new_socket.sendall(("0"+settings.my_username.encode('utf-8')))
	return new_socket # e.g. <socket>

#This function tries to connect with active hosts on the network. If it connects to it
#then it sends the name as a first message and connection request.  
def connected_sockets(): # return a dictionary of connected hosts
	my_ip = helper.get_my_ip() # get my ip from the helper
	ip_list = helper.active_ip_adresses() # get a list of active ip addresses
	for host in ip_list: # iterate over active ips
		try:
			if host != my_ip: # create all sockets if not exist except my own
				new_socket = create_socket(host) # create socket if possible
		except:
			pass # skip if cannot connect to the host

def send_message(host,mess_type, message): # sends message from this host to the other
	# if not current_sockets.get(host, None): # check if this socket already exists
	# 	current_sockets = connected_sockets(username) # create new sockets
	my_socket = settings.current_sockets.get(host)[1] # get socket from sockets dict where key=host, value=(username, socket)
	my_socket.sendall((str(mess_type) + message).encode('utf-8')) # send message using this socket
	if mess_type == 1:
		my_socket.close()
		del settings.current_sockets[host]
	return message