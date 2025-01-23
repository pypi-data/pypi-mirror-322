import threading
from taior.server import start_server
from taior.client import send_file 
from taior.network import add_peer, get_peers, resolve_node_id, load_peers
from cryptography.hazmat.primitives.asymmetric import x25519
import os
import tkinter as tk
from tkinter import filedialog

def main():
    load_peers() 
    choice = input("¿Deseas iniciar como [s]ervidor o [c]liente? ").lower()
    
    private_key = x25519.X25519PrivateKey.generate()

    if choice == 's':
        port = int(input("Introduce el puerto del servidor: "))  
        server_thread = threading.Thread(target=start_server, args=(port,))  
        server_thread.start()
    elif choice == 'c':
        node_id = input("Introduce el identificador del peer (taior://...): ").strip()
        
        root = tk.Tk()
        root.withdraw()  
        file_path = filedialog.askopenfilename(title="Selecciona el archivo a enviar")  
        
        peer_info = resolve_node_id(node_id)
        if peer_info:
            send_file(node_id, file_path, private_key)  
        else:
            print(f"[!] Nodo {node_id} no encontrado.")
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()