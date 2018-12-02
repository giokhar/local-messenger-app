import socket
import threading

def handle_new_client(conn, addr):
	print("by")
	while True:
	    data = conn.recv(1024)
	    if not data: break
	    print("hey")
	    print("Recieved: "+(data.decode('utf-8')))
	    response = input("Reply: ")

	    if response == "exit":
	        break

	    conn.sendall(response.encode('utf-8'))
	conn.close()

host = socket.gethostname()
port = 50010
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

while True:
	conn, addr = s.accept()
	print ("Connection from", addr)
	new_client_thread = threading.Thread(target = handle_new_client, args = (conn,addr,))
	new_client_thread.start()
s.close()
