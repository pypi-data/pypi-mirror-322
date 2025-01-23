import socket
from taior.network import resolve_node_id, select_fast_nodes 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
from taior.crypto import encrypt_data, decrypt_data, generate_private_key, derive_shared_key, encrypt_with_layers
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import x25519, rsa, padding

def send_file_via_multiple_nodes(file_path):
    """Envía un archivo a través de múltiples nodos."""
    fast_nodes = select_fast_nodes(num_nodes=3) 
    for node in fast_nodes:
        send_file(node[0], file_path) 

def send_file(node_id, file_path, private_key, num_layers=3):
    """Conecta con un nodo y envía un archivo cifrado a través de múltiples nodos."""
    peer_info = resolve_node_id(node_id)
    if peer_info:
        host, port = peer_info
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
            
            client_private_key = generate_private_key()
            client_public_key = client_private_key.public_key()
            client.send(client_public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            ))

            peer_public_key_bytes = client.recv(32)
            if len(peer_public_key_bytes) != 32:
                raise ValueError("La clave pública del peer no tiene 32 bytes.")

            peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_key_bytes)

            encrypted_client_public_key = peer_public_key.encrypt(
                client_public_key.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw
                ),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            client.send(encrypted_client_public_key)

            keys = [generate_private_key().exchange(peer_public_key) for _ in range(num_layers)]

            with open(file_path, 'rb') as f:
                file_data = f.read()
            encrypted_file_data = encrypt_with_layers(file_data, keys)
            
            file_name = os.path.basename(file_path)
            encrypted_file_name = encrypt_data(file_name.encode('utf-8'), keys[-1])  
            client.send(encrypted_file_name) 

            client.sendall(encrypted_file_data)

            print(f"[+] Archivo {file_path} enviado con éxito.")

        except Exception as e:
            print(f"[!] Error al enviar el archivo: {e}")
        finally:
            client.close()
    else:
        print(f"[!] Nodo {node_id} no encontrado.")