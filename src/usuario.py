

class Usuario():
    def __init__(self):
        pass
    
    def enviarMSG(self, mensagemCifrada, destino):
        print("Enviando mensagem para: ", destino)
        print("Mensagem cifrada: ", mensagemCifrada)
    
    def receberMSG(self, mensagemDecrifrada, origem):
        print("Mensagem recebida", mensagemDecrifrada,"de:",origem)
    
             
  