import socket
import threading

nome = "Peer1"
estoque = {
    "maçã": 10,
    "banana": 5,
    "pera": 3
}

print(f"\n{nome} - Estoque local:")
for produto, qtd in estoque.items():
    print(f"  - {produto}: {qtd} unidades")

# === Servidor: escuta consultas ===
def servidor():
    s = socket.socket()
    s.bind(("localhost", 7000))
    s.listen(1)
    conn, _ = s.accept()
    while True:
        msg = conn.recv(1024).decode().strip()
        if not msg:
            continue
        print(f"\nRecebido de outro peer: {msg}")
        qtd = estoque.get(msg, 0)
        resposta = f"{nome} responde: {msg} = {qtd}"
        conn.send(resposta.encode())

# === Cliente: envia consultas ===
def cliente():
    c = socket.socket()
    while True:
        try:
            c.connect(("localhost", 7001))
            break
        except:
            pass  # tenta até conseguir conectar

    while True:
        produto = input("\nDigite o nome do produto: ").strip()
        if produto.lower() == "sair":
            break
        c.send(produto.encode())
        resposta = c.recv(1024).decode()
        print(resposta)

# Inicia as duas threads
threading.Thread(target=servidor, daemon=True).start()
cliente()
