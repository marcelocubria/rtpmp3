import socket
from bitstring import BitArray

UDP_IP = "127.0.0.1"
UDP_PORT = 33332

sock = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes

respuesta = BitArray(data).bin
print(respuesta[0:92])
