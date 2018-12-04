import socket
import subprocess

def get_my_ip(): # returns the public ip address of the current device
	return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0] # e.g. '0.0.0.0'

def get_id(ip=get_my_ip()): # returns the id from the ip
	return ip.split('.')[-1] # e.g. when ip='0.0.0.1' id='1'

def get_ip_no_id(ip=get_my_ip()):
	no_id = ""
	for i in ip.split('.')[:-1]:
		no_id += str(i)+"."
	return no_id[:-1]

def get_ip_range(ip=get_my_ip()): # returns the range of the ip_addresses that have potential to be connected to the same router
	return get_ip_no_id(ip)+".1-255" # e.g: 0.0.0.1-255

def active_ip_adresses(): # returns the list of ip adresses connected to the same router using subprocess and nmap
	ip_range = get_ip_range()
	process = subprocess.Popen(("nmap", "-n","-sn", ip_range, "-oG", "-"), stdout=subprocess.PIPE)
	output = subprocess.check_output(["awk", '/Up$/{print $2}'], stdin=process.stdout)
	list_of_ip_addresses = [ip.decode('utf-8') for ip in output.split()] # decode each binary ip and convert to str
	return list_of_ip_addresses # e.g. ['0.0.0.0', '0.0.0.1'...]
