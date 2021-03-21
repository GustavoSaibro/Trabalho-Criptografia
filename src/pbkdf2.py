from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class GeradorChave():       
    def __init__(self):
        pass
    
    def crypt(self, senha, salt, tamanho: int=32,interacoes: int=100000):
        aux = bytes(senha, "utf-8")  
        salt = salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=tamanho,
            salt=salt,
            iterations=interacoes,            
        )
        senha = kdf.derive(aux)  
        return senha
    
    def verificarSenha(self, senha, salt, tamanho: int=32,interacoes: int=100000):
        aux = bytes(senha, "utf-8")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=tamanho,
            salt=salt,
            iterations=interacoes,
        )
        verificado = kdf.verify(aux,senha)
 

    
    

