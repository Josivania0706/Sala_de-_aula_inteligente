import threading
import socket


def main():

    aluno = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        aluno.connect(('localhost', 7777))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    print('\nConexão estabelecida com Gerenciador!')

    thread = threading.Thread(target=sendMessages, args=[aluno])
    thread.start()
            

def sendMessages(aluno):
    while True:
        try:
            print('\nEntre com os seus dados!\n')
            nome = input('\nEntre com o seu nome: \n')
            numero = input('\nEntre com seu número de identificação: \n')
            identifAluno = nome + '_' + numero
            aluno.send(f'{identifAluno}'.encode('utf-8'))
        except:
            return
            
main()