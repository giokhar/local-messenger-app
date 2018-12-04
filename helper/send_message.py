import socket
 
# host = socket.gethostname()
port = 50010

def send_message_to(host):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.settimeout(0.1)
	s.connect((host, port))
	s.settimeout(None)

	print("Connected to "+(host)+" on port "+str(port))

	s.sendall(mess.encode('utf-8'))

	s.close()

#send_message_to("159.28.41.48")

# def get_free_tcp_port():
#     tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     tcp.bind(('', 0))
#     addr, port = tcp.getsockname()
#     tcp.close()
#     return port