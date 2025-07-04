import socket
import sys
import threading

if len(sys.argv) != 4:
    print("Usage: python my_client_app.py <SERVER_IP> <PORT> <ROLE>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])
ROLE = sys.argv[3].upper()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
client_socket.send(ROLE.encode())  # Send role first

print(f"[{ROLE}] Connected to server at {SERVER_IP}:{PORT}")

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
        except:
            break

if ROLE == "SUBSCRIBER":
    threading.Thread(target=receive_messages, daemon=True).start()

while True:
    msg = input("You: ")
    client_socket.send(msg.encode())
    if msg.strip().lower() == "terminate":
        break

client_socket.close()
