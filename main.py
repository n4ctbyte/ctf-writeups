import sqlite3
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# 1. Parameter dari secure_prefs.xml
RAW_KEY_B64 = "zFQ9GVudkfiHhytpG1zAl2B+DHLhE650mzYFCL+pqSI="
SALT_B64 = "5n581xQBvjFW5FFDwj2stw=="
ITERS = 120000

# Siapkan salt & passphrase dalam bentuk bytes
salt = base64.b64decode(SALT_B64)
passphrase = base64.b64decode(RAW_KEY_B64) # Alternatif jika gagal: RAW_KEY_B64.encode('utf-8')

# 2. Fungsi Derivasi Kunci AES-256
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=ITERS
)
aes_key = kdf.derive(passphrase)
aesgcm = AESGCM(aes_key)

# 3. Fungsi Parser Biner Protobuf Sederhana
def parse_protobuf_body(data: bytes):
    idx = 0
    sender, iv, ciphertext, tag = None, None, None, None
    
    while idx < len(data):
        tag_byte = data[idx]
        idx += 1
        
        # Field 1: Sender (0x0A)
        if tag_byte == 0x0A:
            length = data[idx]
            idx += 1
            sender = data[idx:idx+length].decode('utf-8', errors='ignore')
            idx += length
        # Field 2: IV / Nonce (0x12)
        elif tag_byte == 0x12:
            length = data[idx]
            idx += 1
            iv = data[idx:idx+length]
            idx += length
        # Field 3: Ciphertext (0x1A)
        elif tag_byte == 0x1A:
            length = data[idx]
            idx += 1
            ciphertext = data[idx:idx+length]
            idx += length
        # Field 4: Auth Tag (0x22)
        elif tag_byte == 0x22:
            length = data[idx]
            idx += 1
            tag = data[idx:idx+length]
            idx += length
        else:
            break
            
    return sender, iv, ciphertext, tag

# 4. Membaca Database & Menguji Dekripsi
with open("chat.db-wal", "rb") as f:
    wal_data = f.read()

pos = 0
while True:
    idx = wal_data.find(b"\x12\x0c", pos)
    if idx == -1:
        break
        
    iv = wal_data[idx + 2 : idx + 14]
    
    # Pastikan diikuti marker ciphertext 0x1A
    if idx + 14 < len(wal_data) and wal_data[idx + 14] == 0x1A:
        tag_marker_pos = wal_data.find(b"\x22\x10", idx + 14)
        
        # Batasi pencarian tag agar tidak melompat terlalu jauh (misal maks 600 byte)
        if tag_marker_pos != -1 and (tag_marker_pos - idx) < 600:
            # Tentukan titik mulai ciphertext (antisipasi varint)
            start_ct = (idx + 17) if wal_data[idx + 15] >= 0x80 else (idx + 16)
            ciphertext = wal_data[start_ct : tag_marker_pos]
            tag = wal_data[tag_marker_pos + 2 : tag_marker_pos + 18]
            
            # Coba brute-force ID untuk AAD
            for candidate_id in range(1, 40):
                aad = f"kurir:{candidate_id}".encode('utf-8')
                try:
                    plaintext = aesgcm.decrypt(iv, ciphertext + tag, aad)
                    print(f"[FOUND - rowid {candidate_id}]: {plaintext.decode('utf-8')}")
                    break
                except Exception:
                    pass

    pos = idx + 1