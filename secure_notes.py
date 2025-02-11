import os
import sys
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Dossier pour stocker les notes chiffrées
DATA_DIR = "data/secure_files"
KEY_FILE = "key.txt"

def generate_key():
    """Génère une clé AES et la stocke dans key.txt"""
    key = os.urandom(32)
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Charge la clé AES depuis key.txt"""
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt(text, key):
    """Chiffre un texte en AES-GCM"""
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_text = encryptor.update(text.encode()) + encryptor.finalize()
    return base64.b64encode(iv + encryptor.tag + encrypted_text).decode()

def decrypt(encrypted_text, key):
    """Déchiffre un texte en AES-GCM"""
    data = base64.b64decode(encrypted_text)
    iv, tag, encrypted_text = data[:12], data[12:28], data[28:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_text) + decryptor.finalize()

def save_note(note_name, content):
    """Sauvegarde une note chiffrée"""
    key = load_key()
    encrypted_content = encrypt(content, key)
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    file_path = os.path.join(DATA_DIR, f"{note_name}.enc")
    with open(file_path, "w") as file:
        file.write(encrypted_content)
    print(f"Note '{note_name}' enregistrée !")

def read_note(note_name):
    """Affiche une note déchiffrée"""
    key = load_key()
    file_path = os.path.join(DATA_DIR, f"{note_name}.enc")
    if not os.path.exists(file_path):
        print("Note introuvable !")
        return
    with open(file_path, "r") as file:
        encrypted_content = file.read()
    decrypted_content = decrypt(encrypted_content, key)
    print(f"Contenu de la note '{note_name}':\n{decrypted_content.decode()}")

def delete_note(note_name):
    """Supprime une note"""
    file_path = os.path.join(DATA_DIR, f"{note_name}.enc")
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Note '{note_name}' supprimée.")
    else:
        print("Note introuvable !")

def main():
    """Interface CLI"""
    if len(sys.argv) < 3:
        print("Usage: python secure_notes.py [add|read|delete] [note_name] [content (if add)]")
        return
    command, note_name = sys.argv[1], sys.argv[2]
    if command == "add" and len(sys.argv) > 3:
        save_note(note_name, " ".join(sys.argv[3:]))
    elif command == "read":
        read_note(note_name)
    elif command == "delete":
        delete_note(note_name)
    else:
        print("Commande invalide")

if __name__ == "__main__":
    main()
