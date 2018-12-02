import socket
 
host = '127.0.0.1'
port = 50008
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print ("Connection from", addr)
while True:
    data = conn.recv(1024)
    if not data: break
    print("Recieved: "+(data))
    response = input("Reply: ")
    if response == "exit":
        break
    conn.sendall(response)
conn.close()
