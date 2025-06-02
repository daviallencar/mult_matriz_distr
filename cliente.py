import socket
import threading
import pickle
import numpy as np

def start_master_client(matrix_A, matrix_B, worker_addresses):
    n_parts = len(worker_addresses)
    split_A = np.array_split(matrix_A, n_parts)
    result_parts = [None] * n_parts

    def send_to_worker(index, sub_A, B, addr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(addr)
            sock.sendall(pickle.dumps((sub_A, B)))
            data = sock.recv(4096)
            result_parts[index] = pickle.loads(data)

    threads = []
    for i, addr in enumerate(worker_addresses):
        t = threading.Thread(target=send_to_worker, args=(i, split_A[i], matrix_B, addr))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return np.vstack(result_parts)

if __name__ == "__main__":
    A = np.random.randint(1, 10, (4, 4))
    B = np.random.randint(1, 10, (4, 4))
    workers = [('localhost', 5001), ('localhost', 5002)]
    result = start_master_client(A, B, workers)
    print("Matriz A:\n", A)
    print("Matriz B:\n", B)
    print("Resultado A x B:\n", result)
