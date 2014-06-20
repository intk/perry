import sys
import socket

PORT = 50000

msg = sys.argv[1] or "HELLO"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(msg, ('255.255.255.255', PORT))
