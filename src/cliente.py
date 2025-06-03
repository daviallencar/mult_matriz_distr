import socket
import threading
import pickle
import struct
import numpy as np
import time
import csv
import matplotlib.pyplot as plt

def send_all(sock, data):
    length = struct.pack('>I', len(data))  # 4 bytes big-endian
    sock.sendall(length + data)

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('Conexão encerrada antes de receber todos os dados.')
        data += more
    return data

def recv_msg(sock):
    raw_msglen = recv_all(sock, 4)
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recv_all(sock, msglen)

def start_master_client(matrix_A, matrix_B, worker_addresses):
    n_parts = len(worker_addresses)
    split_A = np.array_split(matrix_A, n_parts)
    result_parts = [None] * n_parts

    def send_to_worker(index, sub_A, B, addr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(addr)
            payload = pickle.dumps((sub_A, B))
            send_all(sock, payload)
            result_data = recv_msg(sock)
            result_parts[index] = pickle.loads(result_data)

    threads = []
    for i, addr in enumerate(worker_addresses):
        t = threading.Thread(target=send_to_worker, args=(i, split_A[i], matrix_B, addr))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return np.vstack(result_parts)

if __name__ == "__main__":
    workers = [('localhost', 5001), ('localhost', 5002)]
    sizes = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    results = []

    for size in sizes:
        A = np.random.randint(1, 10, (size, size))
        B = np.random.randint(1, 10, (size, size))

        start_dist = time.time()
        result_dist = start_master_client(A, B, workers)
        end_dist = time.time()
        dist_time = end_dist - start_dist

        start_local = time.time()
        result_local = np.dot(A, B)
        end_local = time.time()
        local_time = end_local - start_local

        results.append([size, dist_time, local_time])

        # Exibir resultado da matriz para verificação
        print(f"\n--- Resultado para matriz {size}x{size} ---")
        print("Matriz A:")
        print(A)
        print("Matriz B:")
        print(B)
        print("Resultado distribuído (A x B):")
        print(result_dist)
        print("Resultado local (A x B):")
        print(result_local)

    # Salvar resultados no CSV
    with open("resultados.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tamanho da Matriz", "Tempo Distribuído (s)", "Tempo Local (s)"])
        writer.writerows(results)

    print("\n[✔] Resultados salvos em 'resultados.csv'")

    # Gerar gráfico comparativo
    tamanhos = [row[0] for row in results]
    tempos_dist = [row[1] for row in results]
    tempos_local = [row[2] for row in results]

    plt.plot(tamanhos, tempos_dist, marker='o', label='Distribuído')
    plt.plot(tamanhos, tempos_local, marker='s', label='Local (Serial)')
    plt.xlabel('Tamanho da Matriz (N x N)')
    plt.ylabel('Tempo (s)')
    plt.title('Comparativo de Desempenho: Distribuído vs Local')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
