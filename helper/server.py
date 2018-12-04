import socket
import threading

def handle_new_client(conn, addr):
	while True:
		data = conn.recv(1024)
		if not data: break
		dec_data = data.decode('utf-8')
		print("Recieved: "+ dec_data)

		if dec_data == "exit":
			break
			
	conn.close()

def receive_new_message():
	host = socket.gethostbyname(socket.gethostname())
	print(host)
	port = 50010
	 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(6)

	while True:
		conn, addr = s.accept()
		print ("Connection from", addr)
		#A thread shuts down itself after handling new client.
		new_client_thread = threading.Thread(target = handle_new_client, args = (conn,addr,))
		new_client_thread.start()
	s.close()

receive_new_message()