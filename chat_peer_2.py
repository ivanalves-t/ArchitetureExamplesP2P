import socket
import threading
import time

NOME = "Peer2" # Remetente Peer 2
MEU_IP = "localhost"
MINHA_PORTA = 6001
PORTA_PEER = 6000 # Destinatário Peer 1

def servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((MEU_IP, MINHA_PORTA))
    s.listen(1)
    print(f"[{NOME}] Esperando conexão na porta {MINHA_PORTA}...")
    conn, _ = s.accept()
    print(f"[{NOME}] Conexão recebida.")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg:
                print(f"\n[Recebido]: {msg}")
                if msg.strip().lower().endswith("sair"):
                    print("[Aviso] O outro peer saiu.")
                    break
        except:
            break

def cliente():
    time.sleep(1)
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            c.connect((MEU_IP, PORTA_PEER))
            break
        except:
            time.sleep(1)
    print(f"[{NOME}] Conectado ao outro peer.")
    while True:
        msg = input("Você (peer_2): ")
        c.send(f"{NOME}: {msg}".encode())
        if msg.strip().lower().endswith("sair"):

            break

threading.Thread(target=servidor, daemon=True).start()
cliente()
