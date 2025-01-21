import socket
from taior.network import resolve_node_id 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
from taior.crypto import encrypt_data, decrypt_data, generate_private_key, derive_shared_key
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

def send_file(node_id, file_path, private_key):
    """Conecta con un nodo y envía un archivo cifrado."""
    peer_info = resolve_node_id(node_id)
    if peer_info:
        host, port = peer_info
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
            
            # Generar la clave privada y pública del cliente
            client_private_key = generate_private_key()
            client_public_key = client_private_key.public_key()

            # Enviar la clave pública al peer
            client.send(client_public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            ))

            # Recibir la clave pública del peer
            peer_public_key_bytes = client.recv(32)
            if len(peer_public_key_bytes) != 32:
                raise ValueError("La clave pública del peer no tiene 32 bytes.")

            peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_key_bytes)

            # Derivar la clave compartida
            shared_key = derive_shared_key(client_private_key, peer_public_key)

            # Leer y cifrar el archivo
            with open(file_path, 'rb') as f:
                file_data = f.read()
            encrypted_file_data = encrypt_data(file_data, shared_key)  # Asegúrate de que file_data sea bytes
            
            # Enviar el nombre del archivo
            file_name = os.path.basename(file_path)
            client.send(file_name.encode('utf-8') + b'\n')  # Enviar el nombre del archivo seguido de un salto de línea

            # Enviar el archivo cifrado
            client.sendall(encrypted_file_data)

            print(f"[+] Archivo {file_path} enviado con éxito.")

        except Exception as e:
            print(f"[!] Error al enviar el archivo: {e}")
        finally:
            client.close()
    else:
        print(f"[!] Nodo {node_id} no encontrado.")