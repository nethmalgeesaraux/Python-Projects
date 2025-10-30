

import argparse
import base64
import getpass
import json
import os
import sys
from typing import Dict, Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.backends import default_backend
import secrets

VAULT_PATH_DEFAULT = "vault.json"
KDF_ITERATIONS = 200_000 
SALT_SIZE = 16  


def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a 32-byte key from the master password and salt, return base64-urlsafe key for Fernet."""
    password_bytes = master_password.encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend(),
    )
    key = kdf.derive(password_bytes)
    return base64.urlsafe_b64encode(key)


def _read_vault_file(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Vault file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_vault_file(path: str, obj: Dict[str, Any]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def init_vault(path: str, master_password: str):
    if os.path.exists(path):
        print("Vault already exists at", path)
        return
    salt = secrets.token_bytes(SALT_SIZE)
    key = derive_key(master_password, salt)
    f = Fernet(key)
    empty = {}
    token = f.encrypt(json.dumps(empty).encode("utf-8"))
    payload = {
        "salt": base64.b64encode(salt).decode("utf-8"),
        "data": base64.b64encode(token).decode("utf-8"),
    }
    _write_vault_file(path, payload)
    print("Initialized new vault at", path)


def load_vault(path: str, master_password: str) -> Dict[str, Dict[str, str]]:
    obj = _read_vault_file(path)
    salt = base64.b64decode(obj["salt"])
    token = base64.b64decode(obj["data"])
    key = derive_key(master_password, salt)
    f = Fernet(key)
    try:
        plaintext = f.decrypt(token)
    except Exception:
        raise ValueError("Incorrect master password or corrupted vault.")
    vault = json.loads(plaintext.decode("utf-8"))
    # Expected vault format: { "site_or_label": { "username": "...", "password": "...", "notes": "..." }, ... }
    return vault


def save_vault(path: str, master_password: str, vault: Dict[str, Dict[str, str]]):
    obj = _read_vault_file(path)
    salt = base64.b64decode(obj["salt"])
    key = derive_key(master_password, salt)
    f = Fernet(key)
    token = f.encrypt(json.dumps(vault).encode("utf-8"))
    new_obj = {
        "salt": base64.b64encode(salt).decode("utf-8"),
        "data": base64.b64encode(token).decode("utf-8"),
    }
    _write_vault_file(path, new_obj)


def add_entry(path: str, master_password: str, label: str, username: str, password: str, notes: str):
    vault = load_vault(path, master_password)
    if label in vault:
        print(f"Warning: '{label}' already exists and will be overwritten.")
    vault[label] = {"username": username, "password": password, "notes": notes}
    save_vault(path, master_password, vault)
    print("Saved entry:", label)


def get_entry(path: str, master_password: str, label: str):
    vault = load_vault(path, master_password)
    item = vault.get(label)
    if not item:
        print(f"No entry named '{label}' found.")
        return
    print("Entry:", label)
    print("  Username:", item.get("username"))
    print("  Password:", item.get("password"))
    notes = item.get("notes")
    if notes:
        print("  Notes:", notes)


def list_entries(path: str, master_password: str):
    vault = load_vault(path, master_password)
    if not vault:
        print("Vault empty.")
        return
    print("Entries:")
    for label in sorted(vault.keys()):
        print(" -", label)


def delete_entry(path: str, master_password: str, label: str):
    vault = load_vault(path, master_password)
    if label not in vault:
        print(f"No entry named '{label}'.")
        return
    del vault[label]
    save_vault(path, master_password, vault)
    print("Deleted entry:", label)


def change_master(path: str, old_master: str, new_master: str):
    vault = load_vault(path, old_master)  # will raise if old_master wrong
    # create new salt for additional safety (so new master has new salt)
    new_salt = secrets.token_bytes(SALT_SIZE)
    new_key = derive_key(new_master, new_salt)
    f = Fernet(new_key)
    encrypted = f.encrypt(json.dumps(vault).encode("utf-8"))
    payload = {
        "salt": base64.b64encode(new_salt).decode("utf-8"),
        "data": base64.b64encode(encrypted).decode("utf-8"),
    }
    _write_vault_file(path, payload)
    print("Master password changed and vault re-encrypted.")


def export_vault(path: str, master_password: str, out_path: str):
    # Export the encrypted vault file as-is; it remains encrypted, safe to move.
    if not os.path.exists(path):
        print("Vault not found:", path)
        return
    # verify password
    _ = load_vault(path, master_password)  # verify
    with open(path, "r", encoding="utf-8") as fin:
        data = fin.read()
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write(data)
    print("Exported encrypted vault to", out_path)


def import_vault(path: str, master_password: str, in_path: str):
    if not os.path.exists(in_path):
        print("File not found:", in_path)
        return
    with open(in_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    # Verify that the provided master password can decrypt the imported file
    salt = base64.b64decode(payload["salt"])
    token = base64.b64decode(payload["data"])
    key = derive_key(master_password, salt)
    fernet = Fernet(key)
    try:
        fernet.decrypt(token)
    except Exception:
        print("Given master password cannot decrypt the imported vault (wrong password?).")
        return
    # Save as current vault file (overwrite)
    _write_vault_file(path, payload)
    print("Imported vault saved to", path)


def main():
    p = argparse.ArgumentParser(description="Simple CLI Password Manager")
    p.add_argument("--vault", default=VAULT_PATH_DEFAULT, help="path to vault file (default: vault.json)")

    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("init", help="initialize a new vault")

    add_p = sub.add_parser("add", help="add/update an entry")
    add_p.add_argument("label", help="label/name for the entry (eg gmail)")

    get_p = sub.add_parser("get", help="retrieve an entry")
    get_p.add_argument("label", help="label to retrieve")

    sub.add_parser("list", help="list entries")

    del_p = sub.add_parser("delete", help="delete an entry")
    del_p.add_argument("label", help="label to delete")

    sub.add_parser("change-master", help="change the master password")
    exp = sub.add_parser("export", help="export encrypted vault to a file")
    exp.add_argument("out", help="output path (eg vault_export.json)")
    imp = sub.add_parser("import", help="import encrypted vault from a file")
    imp.add_argument("infile", help="input path (eg vault_export.json)")

    args = p.parse_args()

    if args.cmd is None:
        p.print_help()
        sys.exit(1)

    vault_path = args.vault

    try:
        if args.cmd == "init":
            master = getpass.getpass("Choose a master password: ")
            confirm = getpass.getpass("Confirm master password: ")
            if not constant_time.bytes_eq(master.encode(), confirm.encode()):
                print("Passwords do not match. Aborting.")
                return
            init_vault(vault_path, master)

        elif args.cmd == "add":
            master = getpass.getpass("Master password: ")
            label = args.label
            username = input("Username: ")
            pw = getpass.getpass("Password (leave empty to generate random): ")
            if not pw:
                # generate a 16-character random password
                pw = base64.urlsafe_b64encode(os.urandom(12)).decode("utf-8").rstrip("=")
                print("Generated password:", pw)
            notes = input("Notes (optional): ")
            add_entry(vault_path, master, label, username, pw, notes)

        elif args.cmd == "get":
            master = getpass.getpass("Master password: ")
            get_entry(vault_path, master, args.label)

        elif args.cmd == "list":
            master = getpass.getpass("Master password: ")
            list_entries(vault_path, master)

        elif args.cmd == "delete":
            master = getpass.getpass("Master password: ")
            confirm = input(f"Really delete '{args.label}'? Type YES to confirm: ")
            if confirm == "YES":
                delete_entry(vault_path, master, args.label)
            else:
                print("Delete cancelled.")

        elif args.cmd == "change-master":
            old = getpass.getpass("Current master password: ")
            new = getpass.getpass("New master password: ")
            confirm = getpass.getpass("Confirm new master password: ")
            if not constant_time.bytes_eq(new.encode(), confirm.encode()):
                print("New passwords do not match. Aborting.")
                return
            change_master(vault_path, old, new)

        elif args.cmd == "export":
            master = getpass.getpass("Master password: ")
            export_vault(vault_path, master, args.out)

        elif args.cmd == "import":
            master = getpass.getpass("Master password for imported vault: ")
            import_vault(vault_path, master, args.infile)
        else:
            print("Unknown command.")
    except FileNotFoundError as e:
        print("Error:", e)
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
