import helper
import socket
import send_message

def create_socket(host, port=50010): # creates sockets if connection is possible in less than 0.2 seconds
	new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an empty socket
	new_socket.settimeout(0.2)
	new_socket.connect((host, port)) # if connection takes more than 0.2 seconds do not connect
	new_socket.settimeout(None)
	return new_socket # e.g. <socket>

def connected_sockets(): # return a dictionary of connected hosts
	my_ip = helper.get_my_ip() # get my ip from the helper
	ip_list = helper.active_ip_adresses() # get a list of active ip addresses
	active_sockets = {} # dictionary to keep track of active sockets
	for host in ip_list: # iterate over active ips
		try:
			if host != my_ip: # create all sockets except my own
				new_socket = create_socket(host) # create socket if possible
				active_sockets[host] = new_socket # {'0.0.0.0':<socket>}
		except:
			pass # skip if cannot connect to the host
	return active_sockets # e.g. {'0.0.0.0':<socket1>, '0.0.0.1':<socket2>, ...}

def send_message(host, message):
	active_sockets = connected_sockets()
	my_socket = active_sockets.get(host)
	my_socket.sendall(message.encode('utf-8'))
	if message == "exit":
		my_socket.close()
	return message

print(send_message('192.168.16.102', "exit"))