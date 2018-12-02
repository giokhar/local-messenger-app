import socket
 
host = socket.gethostname()
port = 50010
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Connected to "+(host)+" on port "+str(port))
initialMessage = input("Send: ")
s.sendall(initialMessage.encode('utf-8'))
 
while True:
	data = s.recv(1024)
	print("Recieved: "+(data.decode('utf-8')))
	response = input("Reply: ")
	if response == "exit":
	 break
	s.sendall(response.encode('utf-8'))
s.close()

# def get_free_tcp_port():
#     tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     tcp.bind(('', 0))
#     addr, port = tcp.getsockname()
#     tcp.close()
#     return port

# def send_message(ip_to_send, port = 50009,  )