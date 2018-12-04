import socket
 
# host = socket.gethostname()
port = 50010
 
def send_message_to(host):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	print("Connected to "+(host)+" on port "+str(port))

	while True:
		initialMessage = input("Send: ")
		s.sendall(initialMessage.encode('utf-8'))
		if initalMessage == "exit":
			break
		#need to break when EXIT is entered

	s.close()

# def get_free_tcp_port():
#     tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     tcp.bind(('', 0))
#     addr, port = tcp.getsockname()
#     tcp.close()
#     return port