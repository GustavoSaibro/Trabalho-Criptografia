from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
import base64

class Criptografia():    
    def __init__(self):
        pass
    
    def encryptGCM(self, text, chave, nonce, aad=None):       
        msg = bytes(text, 'utf-8')
        aesgcm = AESGCM(chave)
        ct = aesgcm.encrypt(nonce, msg, aad)
        return ct

    def decryptGCM(self, chave, ct, nonce, aad=None):
        aesgcm = AESGCM(chave)
        ct = aesgcm.decrypt(nonce, ct, aad)
        return ct

    def encryptCBC(self, chave, iv, mensagem):
        msg = bytes(mensagem, 'utf-8')
        msg = msg[2:len(msg)-1]
        cipher = Cipher(algorithms.AES(chave), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(mensagem) + encryptor.finalize()
        return ct
    
    def decryptCBC(self,chave, iv, ct):
        cipher = Cipher(algorithms.AES(chave), modes.CBC(iv))
        decryptor = cipher.decryptor()
        msg = decryptor.update(ct) + decryptor.finalize()
        return msg
    
    def encryptCTR(self, chave, nonce, mensagem):
        msg = bytes(mensagem, 'utf-8')
        msg = msg[2:len(msg)-1]
        cipher = Cipher(algorithms.AES(chave), modes.CTR(nonce))
        encryptor = cipher.encryptor()
        ct = encryptor.update(mensagem) + encryptor.finalize()
        return ct
    
    def decryptCTR(self, chave, nonce, ct):
        cipher = Cipher(algorithms.AES(chave), modes.CTR(nonce))
        decryptor = cipher.decryptor()
        msg = decryptor.update(ct) + decryptor.finalize()
        return msg

    
