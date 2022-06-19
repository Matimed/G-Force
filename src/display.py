import sys
import os


class Display:
	EXIT_METHODS=[]

	@classmethod
	def add_exit_methods(cls, methods:list): cls.EXIT_METHODS.extend(methods)
    

	@classmethod
	def exit(cls):
		[method() for method in cls.EXIT_METHODS]
    
    
	@classmethod
	def ask(cls, question: str=''):
		""" Receives a question, asks it to the user and returns his answer.
			Also catches the user's exit attempts 
			and redirects them to the save method.
		"""

		if question: print(question)
		answ = input()
		print('')

		if answ == 'quit' or answ == 'exit': cls.exit()
		else: return answ


	@classmethod
	def execute_operation(cls, msg, method, *args):
		print(f"{msg}...\r", end='') 
		result = method(*args)
		print("Operation completed!")
		cls.clear()
		return result


	@staticmethod
	def clear(): os.system('cls' if os.name=='nt' else 'clear')


	@staticmethod
	def list_to_str(list):
		""" Receives a list and returns a human-readable string of elements.
		"""
		string = ''
		for element in list:
			string += str(element) + ' \n'
		return string


	@staticmethod
	def enum_to_list(enum):
		""" Returns the list of all the elements 
			of a given enum and its values.
		"""
        
		return [f'{str(element.value)}: {str(element)}' for element in enum]
        
        
	@staticmethod
	def error_message(response, exception=""):
		print(
			'\033[91m' 
			+ response 
			+ ('\n' if exception else '')
			+ f"{exception}" 
			+ '\033[0m', 
			end='\n\n'
			)

	
	@staticmethod
	def success_message(msg): print('\033[92m' + msg + '\033[0m', end='\n\n')
