known_peers = [("localhost", 5000), ("localhost", 5001)]

def get_peers():
    """Obtiene la lista de nodos conocidos."""
    return known_peers

def add_peer(ip, port):
    """Agrega un nodo a la lista de pares conocidos."""
    if (ip, port) not in known_peers:
        known_peers.append((ip, port))
        print(f"[*] Nodo añadido: {ip}:{port}")
