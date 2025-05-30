from charm.toolbox.pairinggroup import PairingGroup
from charm.core.engine.util import objectToBytes
from cpabe_hybrid import CPABEHybrid
from abe_setup import load_key
import sqlite3
import os




DB_FILE = 'db.sqlite'




def save_ciphertext_to_db(policy, ciphertext_aes_bytes, ciphertext_abe_bytes):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
    INSERT INTO encrypted_data (policy, ciphertext_aes, ciphertext_abe) VALUES (?, ?, ?)
    ''', (policy, ciphertext_aes_bytes, ciphertext_abe_bytes))
    conn.commit()
    conn.close()
    print("[*] Ciphertext saved to database.")




def save_ciphertext(filepath, ct_bytes):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(ct_bytes)




def main():
    group = PairingGroup('SS512')
    cpabe = CPABEHybrid(group)




    # โหลด public key
    pk = load_key('keys/pk.key', group)




    policy = '((doctor or nurse) and (researcher or admin))'
    plaintext = "This is a secret message from doctor to researcher."




    # เข้ารหัสแบบ Hybrid (AES + CP-ABE)
    ciphertext_aes, ct_cpabe = cpabe.encrypt(pk, policy, plaintext)




    # แปลง ciphertext เป็น bytes สำหรับบันทึก
    ciphertext_aes_bytes = ciphertext_aes.encode()   # ciphertext_aes ควรเป็น bytes อยู่แล้ว
    ciphertext_abe_bytes = objectToBytes(ct_cpabe, group)




    # บันทึก ciphertext ลงไฟล์ (ถ้าต้องการ)
    save_ciphertext('ciphertexts/ciphertext_aes.bin', ciphertext_aes_bytes)
    save_ciphertext('ciphertexts/ct_cpabe.bin', ciphertext_abe_bytes)




    # บันทึก ciphertext ลงฐานข้อมูล SQLite
    save_ciphertext_to_db(policy, ciphertext_aes_bytes, ciphertext_abe_bytes)




    print("[*] Encryption done, ciphertext saved to file and database.")




if __name__ == '__main__':
    main()






import sqlite3




DB_FILE = 'db.sqlite'




def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()




    # สร้างตาราง encrypted_data หากยังไม่มี
    c.execute('''
        CREATE TABLE IF NOT EXISTS encrypted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy TEXT NOT NULL,
            ciphertext_aes BLOB NOT NULL,
            ciphertext_abe BLOB NOT NULL
        )
    ''')




    conn.commit()
    conn.close()
    print("[*] Database initialized with table 'encrypted_data'.")




if __name__ == '__main__':
    init_db()



