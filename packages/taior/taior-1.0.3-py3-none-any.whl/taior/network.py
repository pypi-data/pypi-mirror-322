import socket
import threading
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor

known_peers = {}  
routes = {}

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
    known_peers[node_id] = (ip, port) 
    print(f"[*] Nodo añadido/actualizado: {node_id} en {ip}:{port}")
    save_peers() 

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
    """Descubre nuevos nodos en la red compartiendo solo nodos vecinos inmediatos basados en latencia."""
    latencies = measure_latencies(known_peers)  
    sorted_peers = sorted(latencies.items(), key=lambda x: x[1])  
    immediate_neighbors = {node_id: known_peers[node_id] for node_id, _ in sorted_peers[:5]}  # Selecciona los 5 con menor latencia

    for node_id, (ip, port) in immediate_neighbors.items():
        try:
            with socket.create_connection((ip, port), timeout=5) as s:
                s.send(b"GET_NEIGHBORS")
                response = s.recv(1024).decode()
                new_peers = json.loads(response)
                for peer_id, peer_info in new_peers.items():
                    if peer_id not in known_peers:
                        known_peers[peer_id] = tuple(peer_info)
                        print(f"[*] Nuevo nodo vecino descubierto: {peer_id}")
        except (socket.timeout, ConnectionRefusedError):
            print(f"[!] No se pudo conectar con {ip}:{port}")

def measure_latency(peer):
    """Mide la latencia de un nodo enviando un paquete y midiendo el tiempo de respuesta."""
    ip, port = peer[1]
    start_time = time.time()
    try:
        with socket.create_connection((ip, port), timeout=1) as s:
            s.send(b"PING")  
            s.recv(1024)  
    except (socket.timeout, ConnectionRefusedError):
        return float('inf')  
    except Exception as e:
        print(f"[!] Error al medir latencia con {ip}:{port} - {e}")
        return float('inf')  
    return time.time() - start_time 

def measure_latencies(peers):
    """Mide la latencia de múltiples nodos en paralelo."""
    latencies = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(measure_latency, peer): peer for peer in peers.items()}
        for future in futures:
            peer = futures[future]
            try:
                latencies[peer[0]] = future.result()
            except Exception as e:
                print(f"[!] Error al medir latencia para {peer[0]}: {e}")
                latencies[peer[0]] = float('inf')
    return latencies

def select_fast_nodes(num_nodes):
    """Selecciona nodos de alta velocidad para el enrutamiento."""
    latencies = {node_id: measure_latency(peer) for node_id, peer in known_peers.items()}
    sorted_peers = sorted(latencies.items(), key=lambda x: x[1]) 
    return sorted_peers[:num_nodes]

def select_route(num_nodes):
    """Selecciona una ruta a través de múltiples nodos."""
    fast_nodes = select_fast_nodes(num_nodes)  
    return [node[0] for node in fast_nodes]  

def start_peer_server(port):
    """Inicia un servidor simple para compartir la lista de vecinos inmediatos con otros nodos."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen(5)
    print(f"[*] Nodo P2P ejecutándose en el puerto {port}")

    def handle_client(conn, addr):
        print(f"[+] Conexión entrante de {addr}")
        try:
            request = conn.recv(1024).decode()
            if request == "GET_NEIGHBORS":
                latencies = {node_id: measure_latency(peer) for node_id, peer in known_peers.items()}
                sorted_peers = sorted(latencies.items(), key=lambda x: x[1])
                immediate_neighbors = {node_id: known_peers[node_id] for node_id, _ in sorted_peers[:5]}
                conn.send(json.dumps(immediate_neighbors).encode())
        finally:
            conn.close()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
