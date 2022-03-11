import threading
import socket

listaAlunos = []

qntAlunos = 0

msg = ' '

presencaPessoas = '098'
cartaoAlunos = '876'
chaveProjetor = '654'

def main():

    sensor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sensor.connect(('localhost', 7777))
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')

    print('\nConexão estabelecida com Gerenciador!')


    thread1 = threading.Thread(target=receiveMessages, args=[sensor])
  
    thread1.start()

def receiveMessages(sensor):
    global msg

    while True:
        try:
            msg = sensor.recv(2048).decode('utf-8')
            
            #Com base na mensagem recebida, o sensor correto será ativado
            if msg == 'A' or msg == 'a':    #Foi solicitado a lista de alunos
                print('\nEnviar a lista de alunos!\n')
                sensor.send(f'{cartaoAlunos}'.encode('utf-8'))

            elif msg == 'B' or msg == 'b':    #Foi solicitado ligar/desligar o projetor
                print('\nDeve ser alterado o estado do projetor!\n')
                sensor.send(f'{chaveProjetor}'.encode('utf-8'))
            
            #Aluno foi detectado
            elif msg != 'False' and msg != 'A' and msg != 'a':
                listaAlunos.append(msg) 
                print('\nAluno chegou/saiu, dever ser enviado para o Gerenciador!\n')
                sensor.send(f'{presencaPessoas}'.encode('utf-8'))   #Deve-se acender as luzes e o ar condicionado

        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            sensor.close()
            break

main()

