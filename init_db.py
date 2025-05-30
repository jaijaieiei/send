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
