
# 🔗 Multiplicação de Matrizes Distribuída

Este projeto simula um sistema de **computação distribuída** para realizar a **multiplicação de matrizes** usando Python e **sockets TCP**, com um cliente (master) que divide o trabalho entre múltiplos servidores (workers).

---

## 🎯 Objetivo

Demonstrar como distribuir a carga de trabalho da multiplicação de matrizes em vários nós, aproveitando o paralelismo para otimizar o desempenho da operação.

---

## 🧠 Como Funciona

1. O cliente (`cliente.py`) gera duas matrizes A e B.  
2. A matriz A é dividida em blocos de linhas (uma para cada worker).  
3. Cada worker (`servidor.py`) recebe uma fatia de A e a matriz B completa, realiza a multiplicação localmente e envia o resultado de volta.  
4. O cliente reúne as submatrizes recebidas e monta a matriz final.  
5. Tempos de execução local e distribuído são comparados e salvos em `resultados.csv`.  
6. Um gráfico é gerado mostrando a comparação entre os dois métodos.

---

## 🗂️ Estrutura do Projeto

```
mult_matriz_distr/
├── cliente.py          # Cliente principal (master)
├── servidor.py         # Worker genérico (executa multiplicações)
├── resultados.csv      # Resultados de tempo (gerado após execução)
├── Figure_1.png        # Gráficos gerados (opcional)
├── Figure_2.png
├── Figure_3.png
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.6 ou superior  
- Bibliotecas:  
  - `numpy`  
  - `matplotlib`  
  - `pickle`  
  - `socket`  
  - `threading`  
  - `struct`  

Instale as dependências (se necessário):

```bash
pip install numpy matplotlib
```

---

## ▶️ Como Executar

### 1. Inicie os servidores workers

Abra dois terminais separados:

**Terminal 1 (porta 5001):**

```bash
python servidor.py --port 5001
```

**Terminal 2 (porta 5002):**

```bash
python servidor.py --port 5002
```

> Você pode adicionar mais servidores mudando as portas (5003, 5004, ...) e adaptando o código do cliente.

---

### 2. Execute o cliente (master)

**Em um terceiro terminal:**

```bash
python cliente.py
```

Isso irá:

- Gerar matrizes aleatórias com tamanhos crescentes  
- Executar multiplicações de forma local e distribuída  
- Salvar os tempos em `resultados.csv`  
- Exibir gráfico comparativo (serial vs distribuído)

---

## 📊 Exemplo de Saída

```
--- Resultado para matriz 200x200 ---
Matriz A:
[[...]]
Matriz B:
[[...]]
Resultado distribuído (A x B):
[[...]]
Resultado local (A x B):
[[...]]
[✔] Resultados salvos em 'resultados.csv'
```

E um gráfico será exibido ao final com os tempos comparativos.

---

## 🧠 Expansões Possíveis

- Rodar os workers em máquinas diferentes na mesma rede  
- Usar UDP ao invés de TCP para testes  
- Implementar controle de falhas ou balanceamento de carga  
- Multiplicação de matrizes esparsas

---

## 👥 Autores

- [Davi Alencar](https://github.com/daviallencar)  
- [Ana Laura](https://github.com/laurageleilate)

---

> Projeto desenvolvido com fins educacionais para aprendizado de **sistemas distribuídos**, paralelismo e comunicação em rede com Python.
