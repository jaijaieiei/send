from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.core.engine.util import objectToBytes, bytesToObject
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
from CP_ABE import CPabe_BSW07
import hashlib




class CPABEHybrid:
    def __init__(self, group):
        self.group = group
        self.cpabe = CPabe_BSW07(self.group)


    def setup(self):
        return self.cpabe.setup()


    def keygen(self, pk, mk, attributes):
        return self.cpabe.keygen(pk, mk, attributes)


    def encrypt(self, pk, policy_str, plaintext):
        # สร้าง symmetric key แบบสุ่ม
        sym_key = self.group.random(GT)
        key_bytes = objectToBytes(sym_key, self.group)


        # ใช้ SHA-256 เพื่อสร้าง key สำหรับ AES
        digest = hashlib.sha256(key_bytes).digest()
        cipher = SymmetricCryptoAbstraction(digest)


        # เข้ารหัสข้อมูลด้วย AES
        ciphertext_aes = cipher.encrypt(plaintext.encode())


        # เข้ารหัส symmetric key ด้วย CP-ABE
        ct_cpabe = self.cpabe.encrypt(pk, sym_key, policy_str)
        return ciphertext_aes, ct_cpabe


    def decrypt(self, pk, sk, ct_cpabe, ciphertext_aes):
        try:
            # ถอดรหัส symmetric key ด้วย CP-ABE
            sym_key = self.cpabe.decrypt(pk, sk, ct_cpabe)


            # ตรวจว่าถอดรหัสสำเร็จจริงหรือไม่
            if sym_key is None or type(sym_key) != type(self.group.random(GT)):
                return False


            key_bytes = objectToBytes(sym_key, self.group)
            digest = hashlib.sha256(key_bytes).digest()
            cipher = SymmetricCryptoAbstraction(digest)


            plaintext = cipher.decrypt(ciphertext_aes)
            return plaintext.decode()
        except Exception as e:
            print(f"[ERROR] Decryption failed: {e}")
            return False
