#!/usr/bin/env python3
import os
import sys
import socket
import struct
import time
from display import Display


class Server:	
	BUFFER_SIZE = 1024 # Standard of ftp protocol.
	
	def __init__(self, address: tuple[str, int] = ()): 
		self.files_path = "server_files/"
		self.address = address
		self.client_socket = None
		Display.clear()
		try:
			self.client_socket = self.connect()
			self.main()
			
		except KeyboardInterrupt:
			Display.exit()
  
  
	def main(self):
		while True:
			# Enter into a while loop to recieve commands from client
			print("Waiting for instruction . . .\r", end='')
			data = self.recv()
			print("                             \r", end='')
			
			Display.success_message(f"[RECIEVED INSTRUCTION] {data}")
			# Check the command and respond correctly
			match data:
				case "QUIT": self.quit()
				case "UPLOAD": self.upload()
			
			# Reset the data to loop
			data = None
		
	
	def connect(self):
		try:			
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				
				s.bind(self.address)
				print(f"Server socket bind to {self.address}")
				print(f"Waiting for connection...")
				s.listen(1)
				conn , addr = s.accept()		
				Display.clear()	
				Display.success_message(f"[CONNECTED] address={conn.getpeername()}\n")

				return conn
		
		except Exception as e:
			Display.error_message("Connection error:", e)
		
		
	def quit(self):
		try:
			self.send("1") # Send quit conformation
			self.client_socket.close()
			Display.success_message("[DISCONNECTED] Connection has been closed!")
			exit(0)

		
		except Exception as e:
			Display.error_message("[ERROR] Failed to quit!", e)

	
	def upload(self):
		# Send message once server is ready to recieve file details.
		self.send("1")
		# Recieve file name length, then file name.
		file_name_size = struct.unpack("h", self.recv(size=2,decode=False))[0]
		file_name = self.recv(size=file_name_size)
		# Send message to let client know server is ready for document content.
		self.send("1")
		# Recieve file size
		file_size = struct.unpack("i", self.recv(size=4,decode=False))[0]
		# Initialise and enter loop to recive file content
		start_time = time.time()
		with open(self.files_path + file_name, "wb") as output_file:
			# This keeps track of how many bytes we have recieved, so we know when to stop the loop
			Display.success_message(f"\t[RECIEVING FILE] File name: {file_name}")
			bytes_recieved = 0
			while bytes_recieved < file_size:
				file_chunk = self.recv(decode=False)
				output_file.write(file_chunk)
				bytes_recieved += Server.BUFFER_SIZE
		
			Display.success_message(f"\t[RECIEVED FILE] File name: {file_name}")
			
			self.send(struct.pack("f", time.time()-start_time), encode=False)
			self.send(struct.pack("i", file_size), encode=False)
		return


	def send(self, message, encode=True):
		if encode:
			self.client_socket.sendall(message.encode('utf-8'))
		else:
			self.client_socket.sendall(message)
	
	
	def recv(self, size=-1, decode=True): 
		if decode:
			return (self.client_socket.recv(size if size!=-1 else Server.BUFFER_SIZE)).decode('utf-8')
		else:
			return (self.client_socket.recv(size if size!=-1 else Server.BUFFER_SIZE))


if __name__=="__main__":
	default_server_address = ('localhost', 1462) # Random magic number port.
	
	server = Server(default_server_address)
