from charm.toolbox.pairinggroup import PairingGroup


import os
import pickle


from cpabe_hybrid import CPABEHybrid


from charm.core.engine.util import objectToBytes, bytesToObject


def save_key(filepath, key, group):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        key_bytes = objectToBytes(key, group)
        f.write(key_bytes)


def load_key(filepath, group):
    with open(filepath, 'rb') as f:
        key_bytes = f.read()
        key = bytesToObject(key_bytes, group)
    return key


def main():
    group = PairingGroup('SS512')
    cpabe = CPABEHybrid(group)
   
    pk = load_key('keys/pk.key', group)
    mk = load_key('keys/mk.key', group)
   
    users = {
        'alice': ['doctor', 'researcher'],
        'bob': ['nurse'],
        'carol': ['admin']
    }
   
    os.makedirs('keys', exist_ok=True)
   
    for user, attrs in users.items():
        sk = cpabe.keygen(pk, mk, attrs)
        save_key(f'keys/user_{user}.key', sk, group)
        print(f"User '{user}' key with attributes {attrs} saved.")


if __name__ == '__main__':
    main()

