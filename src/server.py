#!/usr/bin/env python3
import os
import sys
import socket
from display import Display


class Server:	
	BUFFER_SIZE = 1024 # Standard of ftp protocol.
	
	def __init__(self, address: tuple[str, int] = ()): 
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
			if data == "QUIT":
				self.quit()
			
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
			Display.manage_exception("Connection error:", e, True)
		
		
	def quit(self):
		try:
			self.send("1") # Send quit conformation
			self.client_socket.close()
			Display.success_message("[DISCONNECTED] Connection has been closed!")
			exit(0)

		
		except Exception as e:
			Display.manage_exception("Failed to quit!", e)


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
