import socket
 
host = '127.0.0.1'
port = 50008
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Connected to "+(host)+" on port "+str(port))
initialMessage = input("Send: ")
s.sendall(initialMessage)
 
while True:
 data = s.recv(1024)
 print("Recieved: "+(data))
 response = input("Reply: ")
 if response == "exit":
     break
 s.sendall(response)
s.close()