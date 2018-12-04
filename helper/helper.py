import socket
import subprocess

def get_my_ip(): # returns the public ip address of the current device
	return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0] # e.g. '0.0.0.0'

def get_ip_range(): # returns the range of the ip_addresses that have potential to be connected to the same router
	ip_range = ""
	my_ip = get_my_ip()
	for i in my_ip.split('.')[0:3]:
		ip_range += str(i)+"."
	ip_range += "1-255"
	return ip_range # e.g: 0.0.0.1-255

def active_ip_adresses(): # returns the list of ip adresses connected to the same router using subprocess and nmap
	ip_range = get_ip_range()
	process = subprocess.Popen(("nmap", "-n","-sn", ip_range, "-oG", "-"), stdout=subprocess.PIPE)
	output = subprocess.check_output(["awk", '/Up$/{print $2}'], stdin=process.stdout)
	list_of_ip_addresses = [ip.decode('utf-8') for ip in output.split()] # decode each binary ip and convert to str
	return list_of_ip_addresses # e.g. ['0.0.0.0', '0.0.0.1'...]