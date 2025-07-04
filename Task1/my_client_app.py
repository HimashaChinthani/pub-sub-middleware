# my_client_app.py
import socket
import sys

if len(sys.argv) != 3:
    print("Usage: python my_client_app.py <SERVER_IP> <PORT>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

print(f"[CLIENT] Connected to server at {SERVER_IP}:{PORT}")

while True:
    message = input("You: ")
    client_socket.send(message.encode())
    if message.strip().lower() == "terminate":
        print("[CLIENT] Termination command sent. Closing connection.")
        break

client_socket.close()
