import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 65432

clients = []

def broadcast(data, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(data)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"Connected to {addr}")
    clients.append(conn)
    try:
        while True:
            header = conn.recv(3)
            if header:
                if header == b'IMG':
                    # Receive image data
                    length = int.from_bytes(conn.recv(4), 'big')
                    img_data = b''
                    while length > 0:
                        chunk = conn.recv(min(length, 2048))
                        img_data += chunk
                        length -= len(chunk)
                    # Broadcast image data to all clients
                    broadcast(b'IMG' + len(img_data).to_bytes(4, 'big') + img_data, conn)
                elif header == b'CLR':
                    # Broadcast clear command to all clients
                    broadcast(b'CLR', conn)
                else:
                    # Receive drawing data
                    data = header + conn.recv(1021)  # 1024 - header length
                    drawing_data = json.loads(data.decode())
                    # Broadcast drawing data to all clients
                    broadcast(data, conn)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        clients.remove(conn)
        print(f"Connection to {addr} closed")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
