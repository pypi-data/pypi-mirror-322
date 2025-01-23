import socket
import threading
import hashlib
from taior.network import add_peer, save_peers, get_peers
from taior.crypto import generate_private_key, derive_shared_key, decrypt_data, encrypt_data
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import x25519, rsa, padding
import json
import uuid
from hashlib import sha256

def generate_node_id():
    """Genera un identificador único de 64 caracteres."""
    return hashlib.sha256().hexdigest()

def handle_client(conn, addr):
    """Maneja una conexión entrante desde un nodo."""
    print(f"[+] Nueva conexión de {addr}")
    try:
        server_private_key = generate_private_key()
        server_public_key = server_private_key.public_key()

        encrypted_client_public_key_bytes = conn.recv(256)  
        client_public_key_bytes = server_private_key.decrypt(
            encrypted_client_public_key_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        client_public_key = x25519.X25519PublicKey.from_public_bytes(client_public_key_bytes)

        conn.send(server_public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ))

        shared_key = derive_shared_key(server_private_key, client_public_key)

        file_name_bytes = b""
        while True:
            byte = conn.recv(1)
            if byte == b'\n': 
                break
            file_name_bytes += byte
        file_name = file_name_bytes.decode('utf-8')

        encrypted_file_data = bytearray()
        while True:
            chunk = conn.recv(4096)  
            if not chunk:
                break
            encrypted_file_data.extend(chunk)

        file_data = decrypt_data(encrypted_file_data, shared_key)

        with open(file_name, 'wb') as f:
            f.write(file_data)

        print(f"[+] Archivo recibido de {addr} y guardado como '{file_name}'.")

    except Exception as e:
        print(f"[-] Error en la conexión con {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Conexión cerrada con {addr}")

def generate_node_id():
    """Genera un identificador de nodo único basado en un UUID."""
    unique_value = str(uuid.uuid4()).encode()  
    return sha256(unique_value).hexdigest()  

def start_server(port):
    """Inicia el servidor para escuchar conexiones entrantes en un puerto específico."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))  
    server.listen(5)
    node_id = generate_node_id()  
    add_peer(f"taior://{node_id}", "localhost", port) 
    save_peers()  

    print(f"[*] Servidor ejecutándose en el puerto {port}")
    print(f"[*] Tu Taior URI es: taior://{node_id}") 

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    port = int(input("Introduce el puerto del servidor: "))
    start_server(port)  