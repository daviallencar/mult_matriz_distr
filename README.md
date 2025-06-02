
# Multiplicação de Matrizes Distribuída

Este projeto simula um sistema de **computação distribuída** para realizar a **multiplicação de matrizes** usando a linguagem Python e comunicação via **sockets TCP** entre um cliente (master) e múltiplos servidores (workers).

## Objetivo

Demonstrar como dividir o trabalho de multiplicação de matrizes entre diferentes "máquinas" (servidores), otimizando a execução de operações matemáticas pesadas de forma paralela.

## Estrutura

- `cliente.py` - Cliente que divide a matriz A, envia partes para os workers e reconstrói o resultado.
- `servidor.py` - Worker que recebe uma parte da matriz A e a matriz B inteira, executa a multiplicação e devolve o resultado.

##  Como funciona

1. O cliente cria duas matrizes A e B.
2. A matriz A é dividida em blocos de linhas e enviada para múltiplos workers.
3. Cada worker calcula sua submatriz resultante: `sub_result = sub_A x B`.
4. O cliente recebe todas as submatrizes e monta o resultado final.

## Como rodar

### 1. Execute dois servidores (em dois terminais diferentes)

No terminal 1 (porta 5001):

```
python servidor.py
```

No terminal 2, altere a porta para 5002 no código `servidor.py`:

```python
start_worker_server(host='localhost', port=5002)
```

E rode:

```
python servidor.py
```

### 2. Execute o cliente (em um terceiro terminal)

```
python cliente.py
```

O cliente irá exibir:

- Matriz A
- Matriz B
- Resultado A x B (calculado de forma distribuída)

## 🔧 Requisitos

- Python 3.6+
- Bibliotecas:
  - `numpy`
  - `pickle`
  - `socket`
  - `threading`

## 📌 Observações

- É possível aumentar o número de workers adicionando mais portas e adaptando o array `workers`.
- A comunicação é feita por TCP/IP localmente (localhost), mas poderia ser expandida para uma rede real.

## 🧑‍💻 Autor

- [Davi Alencar](https://github.com/daviallencar)
- [Ana Laura ](https://github.com/laurageleilate)

---

**Projeto desenvolvido para fins educacionais e de prática em sistemas distribuídos.**
