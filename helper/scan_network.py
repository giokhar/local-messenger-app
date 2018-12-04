import socket
import subprocess
import send_message

def get_my_ip():
	return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

#Returns the range of the ip_addresses that have potential to be connected to the same router.
def get_ip_range():
	ip_range = ""
	#Extracting OWN IP address
	my_ip = get_my_ip()
	for i in my_ip.split('.')[0:3]:
		ip_range += str(i)+"."
	ip_range += "1-255"
	return ip_range

#Returns the list of ip adresses that are active and connected to the same router.
#Using subprocess and nmap. Then parsing the values and moving them into the list.
def active_ip_adresses():
	ip_range = get_ip_range()
	process = subprocess.Popen(("nmap", "-n","-sn", ip_range, "-oG", "-"), stdout=subprocess.PIPE)
	output = subprocess.check_output(["awk", '/Up$/{print $2}'], stdin=process.stdout)
	list_of_ip_addresses = output.split()
	return list_of_ip_addresses

def connect(host, port=50010):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.settimeout(0.1)
	s.connect((host, port))
	s.settimeout(None)

	print("Connected to "+(host)+" on port "+str(port))
	return s

def conn_setup_with_available_hosts():
	ip_list = active_ip_adresses()
	active_socket_list = []
	for next_host in ip_list:
		try:
			active_socket_list.append(connect(next_host.decode('utf-8')))
		except:
			# pass when cannot connect to the next_host
			pass
	send_message.send_message_to(active_socket_list[0], "Rava xar")

conn_setup_with_available_hosts()