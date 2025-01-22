import socket
import threading
import json
import random

known_peers = {}  

def get_peers():
    """Obtiene la lista de nodos conocidos."""
    return known_peers

def load_peers(filename="peers.json"):
    """Carga la lista de nodos conocidos desde un archivo JSON."""
    global known_peers
    try:
        with open(filename, "r") as f:
            loaded_peers = json.load(f)
            known_peers = {k: tuple(v) for k, v in loaded_peers.items()}
            print("[*] Lista de nodos cargada.")
            print(known_peers) 
    except FileNotFoundError:
        print("[!] Archivo de nodos no encontrado. Se usará la lista predeterminada.")

def add_peer(node_id, ip, port):
    """Agrega un nodo a la lista de pares conocidos si no está presente o actualiza el puerto si ya existe."""
    known_peers[node_id] = (ip, port)  # Agrega o actualiza el peer
    print(f"[*] Nodo añadido/actualizado: {node_id} en {ip}:{port}")
    save_peers()  # Guarda la lista de peers en el archivo

def resolve_node_id(node_id):
    """Resuelve un identificador de nodo a una dirección IP y puerto."""
    return known_peers.get(node_id, None) 

def register_node(node_id, ip, port):
    """Registra un nuevo nodo en la red."""
    known_peers[node_id] = (ip, port)
    save_peers()

def save_peers(filename="peers.json"):
    """Guarda la lista de nodos conocidos en un archivo JSON."""
    with open(filename, "w") as f:
        json.dump(known_peers, f)
    print("[*] Lista de nodos guardada.")

def discover_peers():
    """Descubre nuevos nodos en la red."""
    for node_id, (ip, port) in known_peers.items():
        try:
            with socket.create_connection((ip, port), timeout=5) as s:
                s.send(b"GET_PEERS")
                response = s.recv(1024).decode()
                new_peers = json.loads(response)
                for peer_id, peer_info in new_peers.items():
                    if peer_id not in known_peers:
                        known_peers[peer_id] = tuple(peer_info)
                        print(f"[*] Nuevo nodo descubierto: {peer_id}")
        except (socket.timeout, ConnectionRefusedError):
            print(f"[!] No se pudo conectar con {ip}:{port}")

def start_peer_server(port):
    """Inicia un servidor simple para compartir la lista de peers con otros nodos."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen(5)
    print(f"[*] Nodo P2P ejecutándose en el puerto {port}")

    def handle_client(conn, addr):
        print(f"[+] Conexión entrante de {addr}")
        try:
            request = conn.recv(1024).decode()
            if request == "GET_PEERS":
                conn.send(json.dumps(known_peers).encode())
        finally:
            conn.close()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
