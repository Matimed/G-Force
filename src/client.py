#!/usr/bin/env python3
import os
import socket
import struct
import sys
from display import Display
from client_option import Option


class Client:
	BUFFER_SIZE = 1024 # Standard of ftp protocol.
	
	# Default port is a random magic number.
	def __init__(self, server_address: tuple[str, int] = ()): 
		self.files_path = "client_files/"
		
		self.server_address = server_address
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
		
		self.options = {
			Option.CONNECT: self.connect,
			Option.UPLOAD: self.upload,
			Option.QUIT: self.quit,
		}
		
		Display.add_exit_methods([self.quit])
		
		
		Display.clear()
		
		try:
			self.main()
		except KeyboardInterrupt:
			self.exit()
           
           
	def exit(self):
		Display.clear()
		if self.connected():
			Display.exit()
		else: exit(0)


	def connected(self):
		try:
			self.socket.getpeername()
		except Exception as e:
			if e.args[0] == 107: return False
			else: raise(e)
			
		return True
		
		
	def main(self):		
		error=None
		while 1:
			Display.clear()
			if error: Display.error_message("Command not recognised, please try again.", error)
			if self.connected():
				Display.success_message("[Connected]")
			else:
				print("Welcome to the G-Force client!\n")
				
			print("Options:\n")
			print(Display.list_to_str(Display.enum_to_list(Option)))
			option = Display.ask("Select an option:")
			
			try:
				Display.clear()
				self.options[int(option)]() 
				answ = None
				while (answ!="y" and answ!="Y" and answ!=""):
					answ = Display.ask("Continue? [Y/n]")
					print(answ)
					if answ == "n" or answ == "N": self.exit()
					
				error=None
			except Exception as e:
				error = e
				
	
	def connect(self):
		if not self.server_address:
			host = input("Input host (IPv4):")
			port = input("Input port:")
			
			self.server_address = (host, port)
		
		# Connect to the server
		print("Sending server request...")
		try:
			self.socket.connect(self.server_address)
			
			Display.success_message("Connection successful.")
			return
			
		except TypeError as e:
			Display.error_message("Invalid host or port.", e)
		except Exception as e:
			if e.args[0] == 106: # [Errno 106] Transport endpoint is already connected python documentation
				Display.error_message(
					"REFUSED! The connection has already been established.")
			else:
				Display.error_message("Connection unsucessful.", e)


	def quit(self):
		try:
			self.send("QUIT")
			# Wait for server go-ahead
			self.recv()
			self.socket.close()
			Display.success_message("Server connection ended.")
			exit(0)
			
		except Exception as e:
			Display.error_message("Failed closing connection.", e)
			exit(0)
	
	
	def upload(self):
		if not self.connected():
			Display.error_message("No connection to upload a file.")
			return
		
		file_name =  self.files_path + Display.ask("Input file name: ")
		
		try:
			with open(file_name, "rb") as file:
				try:
					self.send("UPLOAD")
				except Exception as e: 
					raise Exception("CUSTOM", "Failed in send instruction.", e)
				
				try:
					self.recv() # Server OK.
					# Send file name size and file name
					self.send(struct.pack("h", sys.getsizeof(os.path.basename(file_name))), encode=False)
					self.send(os.path.basename(file_name))
					self.recv()
					self.send(struct.pack("i", os.path.getsize(file_name)), encode=False)
				except Exception as e: 
					raise Exception("CUSTOM", "Failed sending file details.", e)
					
				try:
					# Send the file in chunks defined by BUFFER_SIZE
					# Doing it this way allows for unlimited potential file sizes to be sent
					print("Sending file...")
					file_chunk = file.read(Client.BUFFER_SIZE)
					while file_chunk:
						self.send(file_chunk, encode=False)
						file_chunk = file.read(Client.BUFFER_SIZE)
				except Exception as e: 
					raise Exception("CUSTOM", "Failed in send file.", e)
		except Exception as e:
			if e.args[0] == "CUSTOM":
				Display.error_message(e.args[1], e.args[2])
			else:
				Display.error_message("Failed in open file.", e)
			
			return
		
		try:
			# Get upload performance details
			upload_time = struct.unpack("f", self.recv(4, decode=False))[0]
			upload_size = struct.unpack("i", self.recv(4, decode=False))[0]
			
			Display.success_message(f"{file_name} sent successfully.")
			print(f"Time elapsed: {upload_time}")
			print(f"File size: {upload_size}b\n")
		except Exception as e:
			Display.error_message("Failed getting upload time.", e)
			return
	
	
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
		
