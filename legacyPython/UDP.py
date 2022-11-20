
import socket
import struct
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def sendUDP(message, IP = "127.0.0.1", port = 8080):
    msgFromClient       = message
    bytesToSend         = str.encode(msgFromClient)
    serverAddressPort   = (IP, port)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)


