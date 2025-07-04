import socket
import sys
import threading

if len(sys.argv) != 5:
    print("Usage: python my_client_app.py <SERVER_IP> <PORT> <ROLE> <TOPIC>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])
ROLE = sys.argv[3].upper()
TOPIC = sys.argv[4].upper()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

# Send role and topic to server
client_socket.send(f"{ROLE} {TOPIC}".encode())

print(f"[{ROLE}] Connected to server on topic: {TOPIC}")

def receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                print(f"\n{msg}")
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
