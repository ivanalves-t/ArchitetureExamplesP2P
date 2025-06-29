import socket
import threading

estoque = {"maçã": 5, "pera": 8}

def servidor():
    s = socket.socket()
    s.bind(("localhost", 8001))
    s.listen(1)
    conn, _ = s.accept()
    while True:
        msg = conn.recv(1024).decode()
        if not msg: break
        print("Peer1 pediu:", msg)
        if msg.startswith("consultar"):
            produto = msg.split()[1]
            qtd = estoque.get(produto, 0)
            conn.send(f"{produto}: {qtd}".encode())
        elif msg == "sair":
            break
    conn.close()

import time

def cliente():
    c = socket.socket()
    while True:
        try:
            c.connect(("localhost", 8000))  # ou 8000 no peer2.py
            break
        except ConnectionRefusedError:
            time.sleep(1)  # espera 1 segundo e tenta de novo
    while True:
        msg = input("Você (peer2): ")
        c.send(msg.encode())
        if msg == "sair": break
        resposta = c.recv(1024).decode()
        print("Resposta:", resposta)
    c.close()


threading.Thread(target=servidor, daemon=True).start()
cliente()
