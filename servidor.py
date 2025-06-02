import socket
import threading
import pickle
import numpy as np

def start_worker_server(host='localhost', port=5002):
    def handle_client(conn, addr):
        data = conn.recv(4096)
        sub_A, B = pickle.loads(data)
        sub_result = np.dot(sub_A, B)
        conn.sendall(pickle.dumps(sub_result))
        conn.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Worker rodando em {host}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_worker_server()
