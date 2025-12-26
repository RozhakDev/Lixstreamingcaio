import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def decrypt_url(encrypted_url: str) -> str:
    """
    Mengubah kembali URL terenkripsi menjadi teks asli yang dapat dibaca.

    Fungsi ini menggunakan algoritma AES-256-CBC untuk membuka proteksi pada URL
    agar aset dapat diakses kembali oleh aplikasi.

    Args:
        encrypted_url (str): String URL dalam format terenkripsi (Base64).

    Returns:
        str: String URL asli yang telah berhasil didekripsi.
    """
    key = "GNgN1lHXIFCQd8hSEZIeqozKInQTFNXj".encode('utf-8')
    iv = "2Xk4dLo38c9Z2Q2a".encode('utf-8') # Source: https://github.com/mycodedoesnotcompile2/jdownloader_mirror/blob/94d8231acc5ed6b6073198b14a2ee60f50027292/svn_trunk/src/jd/plugins/hoster/LixstreamCom.java

    crypted_bytes = base64.b64decode(encrypted_url)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(crypted_bytes) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_bytes = unpadder.update(decrypted_padded) + unpadder.finalize()

    final_url = decrypted_bytes.decode('utf-8')
    return final_url