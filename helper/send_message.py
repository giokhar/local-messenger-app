import socket
 
# host = socket.gethostname()
port = 50010

def send_message_to(active_socket, message):

	active_socket.sendall(message.encode('utf-8'))

	if message == "exit":
		s.close()

#send_message_to("159.28.41.48")

# def get_free_tcp_port():
#     tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     tcp.bind(('', 0))
#     addr, port = tcp.getsockname()
#     tcp.close()
#     return port