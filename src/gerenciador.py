import os
import base64
from cryptography.fernet import Fernet

class Gerenciador():    
    def __init__(self):
        pass
    
    # Criação da chave Fernet
    def chaveCrypt(self):
        chave = Fernet.generate_key()
        return chave
    
    # Metodo para criar o arquivo e escerver nele  
    def wrt(self,nome, chave, nonce, iv, salt,aad):        
        if(os.path.isfile("./chaves/gerenciador.txt")):                
            with open(r"./chaves/gerenciador.txt", "a+") as file:
                file.write("nome: "+nome+" chave: "+chave+" nonce: "+nonce+" iv: "+iv+" salt: "+salt+" aad: "+aad+"\n")
        else:
            with open(r"./chaves/gerenciador.txt", "w+") as file:
                file.write("nome: "+nome+" chave: "+chave+" nonce: "+nonce+" iv: "+iv+" salt: "+salt+" aad: "+aad+"\n")
    
    def wrtMSG(self,nomeDestino,nomeOrigem,mensagem):
        print(os.path.isfile("./mensagem/mensagem.txt"))
        if(os.path.isfile("./mensagem/mensagem.txt")):                
            with open(r"./mensagem/mensagem.txt", "a+") as file:
                file.write("mensagem: "+mensagem+" "+"de "+nomeOrigem+ " para: "+nomeDestino+"\n")
        else:
            with open(r"./mensagem/mensagem.txt", "w+") as file:
                file.write("mensagem: "+mensagem+" "+"de "+nomeOrigem+ " para: "+nomeDestino+"\n")
    
    
    # Retorna true se o arquivo foi criado e false se não
    def arquivoCriado(self,caminho):
        return os.path.isfile(caminho)
    
    # Procura no arquivo se aquele nome passado como parametro está contido no gerenciador
    def acharNome(self,nome,caminho):
        with open(caminho, 'rb') as file: 
            count = 0
            linha = ""        
            while True:
                count += 1            
                linha = file.readline().decode().strip("\n").lower()
                # nome = line.find(nome) 
                palavras = linha.split()
                if nome in  palavras: 
                    return linha   
                if not linha:
                    break
        return linha 
    
    # Procura na linha do usuario selecionado o parametro desejado
    def acharParametros(self,linha: str, parametro):
        palavras = linha.split()
        ind = palavras.index(parametro)
        parametro = palavras[ind+1]        
        return parametro  
  
    # Cifrando o arquivo do gerenciador usando a chave gerada pelo Fernet   
    def fileCrypt(self, chave):
        fernet = Fernet(chave) 
                
        # Abrindo o arquivo original
        with open('./chaves/gerenciador.txt', 'rb') as file: 
            original = file.read() 
            
        # Cifrando o arquivo 
        encrypted = fernet.encrypt(original) 
        
        #Escrevendo o arquivo cifrado
        with open('./chaves/gerenciador.txt', 'wb') as encrypted_file: 
            encrypted_file.write(encrypted)

    # Decifrando o arquivo do gerenciador usando a chave gerada pelo Fernet
    def fileDecrypt(self, chave):
        fernet = Fernet(chave) 
        
        # Abrindo o arquivo cifrado
        with open('./chaves/gerenciador.txt', 'rb') as enc_file: 
            encrypted = enc_file.read() 
        
        # Decifrando o arquivo  
        decrypted = fernet.decrypt(encrypted) 

        # Abrindo e escrevendo o arquivo decrifrado
        with open('./chaves/gerenciador.txt', 'wb') as dec_file: 
            dec_file.write(decrypted)