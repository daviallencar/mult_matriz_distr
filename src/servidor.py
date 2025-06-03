import socket
import threading
import pickle
import struct
import numpy as np
import argparse

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError(f'Esperado {length} bytes, mas conexão foi encerrada prematuramente.')
        data += more
    return data

def handle_client(conn, addr):
    try:
        raw_msglen = recv_all(conn, 4)
        msglen = struct.unpack('>I', raw_msglen)[0]
        data = recv_all(conn, msglen)
        sub_A, B = pickle.loads(data)
        sub_result = np.dot(sub_A, B)

        result_data = pickle.dumps(sub_result)
        result_len = struct.pack('>I', len(result_data))
        conn.sendall(result_len + result_data)
    except Exception as e:
        print(f"[!] Erro no worker {addr}: {e}")
    finally:
        conn.close()

def start_worker_server(host='localhost', port=5001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"[WORKER] Servidor rodando em {host}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor Worker")
    parser.add_argument("--port", type=int, default=5001, help="Porta do servidor")
    args = parser.parse_args()
    start_worker_server(port=args.port)
