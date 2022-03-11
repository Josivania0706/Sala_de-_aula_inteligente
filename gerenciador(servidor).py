import threading
import socket
import time
from datetime import datetime

clients = []                #Lista com todos os clientes conectados
listaAlunosDinâmica = []    #Lista com os alunos para ter 'controle' de quem saiu ou chegou
listaAlunos = []            #Lista com os alunos que estiveram na aula
totalAlunos = 0             #Armazena a quantidade de alunos - total
qntAlunos = 0               #Armazena a quantidade de alunos - para controle
estadoProjetor = 0          #Armazena o estado do projetor

horaAgora = datetime.now()
hora = horaAgora.hour       #Armazena a hora, para que as 23:00 horas, desligue todos os atuadores

luz = '123'                 #Identificador do atuador - Iluminação
projetor = '345'            #Identificador do atuador - Projetor
arCond = '567'              #Identificador do atuador - Ar Condicionado

def main():

    gerenciador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        gerenciador.bind(('localhost', 7777))
        gerenciador.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = gerenciador.accept()
        clients.append(client)

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    global qntAlunos
    global totalAlunos

    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            identificador = 'False'

            if str(hora) == '23':           #Às 23:00 horas, todos os atuadores serão desligados
                desligarTodosAtuadores(client, identificador)

            #Mandar para o Sensor essa informação, para ele saber o que fazer

            if msg == 'A' or msg == 'a':    #Professor requisitou a lista
                enviarSensor(client, msg)

            elif msg == 'B' or msg == 'b':  #O professor deseja ligar/desligar o projetor -> enviar para sensor
                enviarSensor(client, msg)

            elif msg == '876':              #O sensor de Cartão de Alunos foi acionado -> receber do sensor
                retornarLista(client)

            elif msg == '654':              #O sensor de Chave do Projetor foi acionado -> receber do sensor
                ligarProjetor(client, projetor)
                ligarIluminacao(client, luz)
                print('\nO projetor teve seu estado alterado!\n')

            elif msg == '098':              #O sensor de Presença de Pessoas foi acionado -> receber do sensor
                print('\nDetectado aluno na sala!\n')
                if qntAlunos == 1:
                    ligarIluminacao(client, luz)    #Ligar luz quando um aluno chegar
                    ligarArCond(client, arCond)     #Ligar ar condicionado quando um aluno chegar

         
            else:                                   #Chegou/saiu algum aluno
                if msg in listaAlunosDinâmica:      #Aluno saiu
                    qntAlunos -= 1
                    listaAlunosDinâmica.remove(msg)
                    print('\nAluno saiu da sala!\n')
                    if qntAlunos == 0:              #Não tem mais ninguém na sala -> deve-se desligar tudo
                        time.sleep(900)
                        desligarTodosAtuadores(client, identificador)
                else:                               #Aluno chegou
                    qntAlunos += 1
                    totalAlunos += 1
                    enviarSensor(msg, client)       #Enviar para o sensor
                    adicionarAlunos(msg, client)

        except:
            print('\nNão foi possível manter-se conectado!\n')
     
#Envia quantos alunos e o nome dos alunos que participaram da aula
def retornarLista(client):
    for clientItem in clients:
        try:
            clientItem.send(f'_Número de alunos que participaram da aula: {totalAlunos}\nNome dos alunos:\n {listaAlunos}'.encode('utf-8'))
        except:
            print('\nOcorreu algo errado!\n')


def adicionarAlunos(msg, client):
    #Como existe pelo menos um novo aluno, as luzes e o ar condicionado, devem ser ligados
    listaAlunos.append(msg) #Adicionar o novo aluno à lista
    listaAlunosDinâmica.append(msg)


#Funções de acesso aos Atuadores
def ligarIluminacao(client, luz):
    print('\nO atuador Iluminação teve seu estado alterado!\n')

    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(f'{luz}'.encode('utf-8'))
            except:
                print('\nOcorreu algo errado!\n')


def ligarProjetor(client, projetor):
    print('\nO atuador Projetor teve seu estado alterado!\n')

    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(f'{projetor}'.encode('utf-8'))
            except:
                print('\nOcorreu algo errado!\n')


def ligarArCond(client, arCond):
    print('\nO atuador Ar Condicionado teve seu estado alterado!\n')

    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(f'{arCond}'.encode('utf-8'))
            except:
                print('\nOcorreu algo errado!\n')


def enviarSensor(client, msg):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(f'{msg}'.encode('utf-8'))
            except:
                print('\nOcorreu algo errado!\n')


#Função para desligar os Atuadores após 15 minutos
def desligarTodosAtuadores(client, identificador):
    print('\nDesligando todos os atuadores!\n')
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(f'{identificador}'.encode('utf-8'))
            except:
                print('\nOcorreu algo errado!\n')


main()