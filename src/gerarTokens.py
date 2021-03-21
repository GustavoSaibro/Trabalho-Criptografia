import secrets 

class GeradorRandom():    
    def __init__(self):
        pass
    
    def gerarSalt(self, size: int=32):
        salt = secrets.token_bytes(size)
        return salt     
    
    def gerarIV(self, size: int=16):
        iv = secrets.token_bytes(size)
        return iv

    def gerarNonce(self, size: int=12):
        nonce = secrets.token_bytes(size)
        return nonce

    def gerarAAD(self, size: int=16):
        aad = secrets.token_bytes(size)
        return aad