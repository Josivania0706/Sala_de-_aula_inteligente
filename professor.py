import threading
import socket

caractere1 = '_'
caractere2 = '<'

def main():

    profess = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        profess.connect(('localhost', 7777))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    print('\nConexão estabelecida com Gerenciador!')

    thread1 = threading.Thread(target=receiveMessages, args=[profess])
    thread2 = threading.Thread(target=sendMessages, args=[profess])

    thread1.start()
    thread2.start()         

def receiveMessages(profess):
    while True:
        try:
            msg = profess.recv(2048).decode('utf-8')

            #Só serão printadas as frases que começam com '_'
            if caractere1 in msg:
                if caractere2 not in msg:
                    print(msg+'\n')


        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            profess.close()
            break

def sendMessages(profess):
    while True:
        try:
            print('\nA - Requisitar  a lista de alunos presentes.\n')
            print('\nB - Ligar/desligar o projetor.\n')
            msg = input('\n')

            if msg == 'A' or msg == 'a':
                profess.send(f'{msg}'.encode('utf-8'))
            elif msg == 'B' or msg == 'b':
                profess.send(f'{msg}'.encode('utf-8'))
            else:
                print('\nA entrada é inválida!\n')

        except:
            return
            
main()