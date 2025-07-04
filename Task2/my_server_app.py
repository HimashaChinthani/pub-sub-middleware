import socket
import threading
import sys

if len(sys.argv) != 2:
    print("Usage: python my_server_app.py <PORT>")
    sys.exit(1)

HOST = ''
PORT = int(sys.argv[1])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[SERVER] Listening on port {PORT}...")

clients = []  # List of (conn, addr, role)

lock = threading.Lock()

def broadcast(message, sender_conn):
    with lock:
        for client in clients:
            conn, addr, role = client
            if role == "SUBSCRIBER" and conn != sender_conn:
                try:
                    conn.send(message.encode())
                except:
                    conn.close()
                    clients.remove(client)

def handle_client(conn, addr):
    try:
        role = conn.recv(1024).decode().strip().upper()
        print(f"[SERVER] {addr} connected as {role}")

        with lock:
            clients.append((conn, addr, role))

        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[{role} {addr}] says: {msg}")
            if msg.strip().lower() == "terminate":
                break
            if role == "PUBLISHER":
                broadcast(f"[PUBLISHER {addr}]: {msg}", conn)
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        with lock:
            clients[:] = [c for c in clients if c[0] != conn]
        conn.close()
        print(f"[SERVER] {addr} disconnected.")

while True:
    conn, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
