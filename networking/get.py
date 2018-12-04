import socket
import threading
from networking.helper import get_my_ip

def handle_new_client(conn, addr):
	while True:
		data = conn.recv(1024)
		if not data: break
		dec_data = data.decode('utf-8')
		print("Recieved: "+ dec_data)

		if dec_data == "exit":
			break
			
	conn.close()

def listener(socketio, port=50010):
	host = get_my_ip() # method is imported from networking.helper
	print("listening on", host, "port", port)
	 
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((host, port))
	server_socket.listen(6)

	while True:
		conn, addr = server_socket.accept()
		print ("Connection from", addr)
		#A thread shuts down itself after handling new client.
		new_client_thread = threading.Thread(target = handle_new_client, args = (conn,addr,))
		new_client_thread.start()
	server_socket.close()