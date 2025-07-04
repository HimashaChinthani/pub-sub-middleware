# my_server_app.py
import socket
import sys

if len(sys.argv) != 2:
    print("Usage: python my_server_app.py <PORT>")
    sys.exit(1)

PORT = int(sys.argv[1])
HOST = ''  # Accept connections from any address

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[SERVER] Listening on port {PORT}...")

conn, addr = server_socket.accept()
print(f"[SERVER] Connected by {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print(f"[CLIENT]: {data}")
    if data.strip().lower() == "terminate":
        print("[SERVER] Termination signal received. Closing connection.")
        break

conn.close()
server_socket.close()
