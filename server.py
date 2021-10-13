from socket import *
import random

server_name = '0.0.0.0'
server_port = 1200

socket = socket(AF_INET, SOCK_DGRAM)
socket.bind(('', server_port))

print(f"Server is up! Port: {server_name}")

sequence_number = random.randint(1, 9999)

while True:
    message, client_address = socket.recvfrom(2048)
    print(message)
