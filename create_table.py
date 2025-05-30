import sqlite3

DB_FILE = 'db.sqlite'

def create_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
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
    print("[*] Table 'encrypted_data' created (if not exists).")

if __name__ == '__main__':
    create_table()
