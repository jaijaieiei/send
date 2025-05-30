import sqlite3
from cpabe_hybrid import CPABEHybrid
from charm.toolbox.pairinggroup import PairingGroup
from charm.core.engine.util import bytesToObject
from abe_setup import load_key
import sys
import base64


DB_FILE = 'db.sqlite'


def load_ciphertext(id=1, group=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT policy, ciphertext_aes, ciphertext_abe FROM encrypted_data WHERE id=?', (id,))
    row = c.fetchone()
    conn.close()


    if row:
        policy, ciphertext_aes_bytes, ciphertext_abe_bytes = row  # ไม่ต้อง decode base64


        ciphertext_abe = bytesToObject(ciphertext_abe_bytes, group)


        return policy, ciphertext_aes_bytes, ciphertext_abe
    else:
        return None, None, None




def main():
    if len(sys.argv) < 2:
        print("Usage: python decrypt_and_verify.py <user_key_filename>")
        return


    user_key_file = sys.argv[1]


    # ✅ สร้าง group ก่อนโหลด key
    group = PairingGroup('SS512')
    cpabe = CPABEHybrid(group)


    # ✅ โหลด public key และ secret key ด้วย group เดียวกัน
    pk = load_key('keys/pk.key', group)
    sk = load_key(user_key_file, group)


    # ✅ โหลด ciphertext โดยส่ง group เข้าไป
    policy, ciphertext_aes, ciphertext_abe = load_ciphertext(group=group)


    if not policy:
        print("[!] No ciphertext found in database.")
        return


    print(f"[*] Found ciphertext with policy: {policy}")
    print(f"[DEBUG] User secret key attributes: {sk.get('S', 'unknown')}")


    # ✅ ใช้ group เดียวกับทั้งหมด
    plaintext = cpabe.decrypt(pk, sk, ciphertext_abe, ciphertext_aes)


    if plaintext is False:
        print("[!] You are NOT authorized to decrypt this message (policy not satisfied).")
    else:
        print("[*] Decrypted message:", plaintext)




if __name__ == '__main__':
    main()


