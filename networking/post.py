import socket
from networking import settings
from networking import helper
import json

def create_socket(host, port=50011): # creates sockets if connection is possible in less than 0.2 seconds
	new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an empty socket
	#new_socket.settimeout(1) # if connection takes more than 0.2 seconds do not connect
	new_socket.connect((host, port)) # connect using this type (host, port) tuple
	#new_socket.settimeout(None)
	return new_socket # e.g. <socket>

#This function tries to connect with active hosts on the network. If it connects to it
#then it sends the name as a first message and connection request.  
def connected_sockets(): # return a dictionary of connected hosts
	my_ip = helper.get_my_ip() # get my ip from the helper
	ip_list = helper.active_ip_adresses() # get a list of active ip addresses
	print(ip_list)
	for host in ip_list: # iterate over active ips
		try:
			if host != my_ip: # create all sockets if not exist except my own
				send_message(host, 0) # sending just the user name with message_type = 0
		except:
			print("Not", host) # skip if cannot connect to the host

def send_message(host, message_type, message=""):
	data = {"username":settings.my_username,"message_type":str(message_type),"message":message_type}
	new_socket = create_socket(host) # create socket to send a message to the given ip address
	new_socket.sendall(json.dumps(data.encode('utf-8'))) # send json object converted to string and encoded
	new_socket.close() # close current socket
	return data

