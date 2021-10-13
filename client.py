from socket import *

# manda a mensagem e espera uma resposta do server com o resultado do checksum no ack ou nak
# (server que envia de volta) ack para 200 e nak para 500 com relação ao pacote enviado
# caso venha um nak, será necessário reenviar o pacote

# 2.1 -> verifica se o pacote corrompido esta sendo reenviado mais de uma vez

server_name = '0.0.0.0'
server_port = 1200

socket = socket(AF_INET, SOCK_DGRAM)

message = input('Input lowercase sentence: ')
socket.sendto(message.encode(), (server_name, server_port))
# modifiedMessage, serverAddress = socket.recvfrom(2048) print(modifiedMessage.decode())
socket.close()
