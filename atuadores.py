#Classe Atuador

import threading
import socket

#Atuador de iluminação - 123
iluminacao = 'False'

#Atuador de projetor - 345
projetor = 'False'

#Atuador de ar condicionado - 567
arCond = 'False'

def main():	

	atuador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		#Tatar se conectar ao gerenciador, pelo host e com a porta
		atuador.connect(('localhost', 7777))
	
	#Não foi possível se conectar ao gerenciador
	except:
		return print('\nNão foi possível se conectar ao gerenciador, tente novamente mais tarde!\n')

	print('\nConexão estabelecida com Gerenciador!')

	thread = threading.Thread(target=receiveMessages, args=[atuador])
	thread.start()


#Não ocorreu nenhum erro
def receiveMessages(atuador):
	while True:
		try:
			msg = atuador.recv(2048).decode('utf-8')
			if iluminacao == 'False' and msg == '123':					
				alteraLigado(msg)
			elif iluminacao == 'True' and msg == '123':
				alteraDesligado(msg)
			elif projetor == 'False' and msg == '345':
				alteraLigado(msg)
			elif projetor == 'True' and msg == '345':
				alteraDesligado(msg)
			elif arCond == 'False' and msg == '567':
				alteraLigado(msg)
			elif arCond == 'True' and msg == '567':
				alteraDesligado(msg)

			#Verificar se a mensagem recebida vai ser false, para desligar tudo
			elif msg == 'False':
				desligarTodos(msg)

		except:
			print('\nNão foi possível permanecer conectado no servidor!\n')
			atuador.close()
			break


def alteraLigado(msg):
	global iluminacao
	global projetor
	global arCond

	if msg == '123':
		iluminacao = 'True'
		print('\nAs luzes estão ligadas!\n')
	elif msg == '345':
		projetor = 'True'
		print('\nO projetor está ligado!\n')
	elif msg == '567':
		arCond = 'True'
		print('\nO ar condicionado está ligado!\n')

def alteraDesligado(msg):
	global iluminacao
	global projetor
	global arCond
	
	if msg == '123':
		iluminacao = 'False'
		print('\nAs luzes estão desligadas!\n')
	elif msg == '345':
		projetor = 'False'
		print('\nO projetor está desligado!\n')
	elif msg == '567':
		arCond = 'False'
		print('\nO ar condicionado está desligado!\n')


def desligarTodos(msg):
	global iluminacao
	global projetor
	global arCond
	
	if msg == 'False':
		iluminacao = 'False'
		print('\nAs luzes estão desligadas!\n')

		projetor = 'False'
		print('\nO projetor está desligado!\n')

		arCond = 'False'
		print('\nO ar condicionado está desligado!\n')

main()