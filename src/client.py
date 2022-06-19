#!/usr/bin/env python3
import socket
from display import Display
from client_option import Option


class Client:
	BUFFER_SIZE = 1024 # Standard of ftp protocol.
	
	# Default port is a random magic number.
	def __init__(self, server_address: tuple[str, int] = ()): 
		self.server_address = server_address
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
		
		self.options = {
			Option.CONNECT: self.connect,
			Option.QUIT: self.quit,
		}
		
		Display.add_exit_methods([self.quit])
		
		
		Display.clear()
		print("Welcome to the G-Force client!\n")
		
		try:
			self.main()
		except KeyboardInterrupt:
			Display.clear()
			Display.exit()
           
           
	def main(self):		
		while 1:
			print("Options:\n")
			print(Display.list_to_str(Display.enum_to_list(Option)))
			option = Display.ask_question("Select an option:")
			
			try:
				Display.clear()
				self.options[int(option)]() 
			except Exception as e:
				Display.manage_exception("Command not recognised, please try again.", e)
				
	
	def connect(self):
		if not self.server_address:
			host = input("Input host (IPv4):")
			port = input("Input port:")
			
			self.server_address = (host, port)
		
		# Connect to the server
		print("Sending server request...")
		try:
			self.socket.connect(self.server_address)
			Display.clear()
			print("Response:")
			Display.success_message("DONE! Connection sucessful.")
			
		except TypeError as e:
			Display.manage_exception("Invalid host or port.", e)
		except Exception as e:
			if e.args[0] == 106: # [Errno 106] Transport endpoint is already connected python documentation
				Display.manage_exception(
					"REFUSED! The connection has already been established.")
			else:
				Display.manage_exception("Connection unsucessful.", e)
		

	def quit(self):
		try:
			self.send("QUIT")
			# Wait for server go-ahead
			self.recv()
			self.socket.close()
			print("Response:")
			Display.success_message("Server connection ended.")
			exit(0)
			
		except Exception as e:
			Display.manage_exception("Failed in quit.", e)
		
	
	
	def send(self, message, encode=True):
		if encode:
			self.socket.sendall(message.encode('utf-8'))
		else:
			self.socket.sendall(message)
	
	
	def recv(self, size=-1, decode=True): 
		if decode:
			return (self.socket.recv(size if size!=-1 else Client.BUFFER_SIZE)).decode('utf-8')
		else:
			return (self.socket.recv(size if size!=-1 else Client.BUFFER_SIZE))
			
	
if __name__=="__main__":
	default_server_address = ('localhost', 1462) # Random magic number port.
	
	client = Client(default_server_address)
		
