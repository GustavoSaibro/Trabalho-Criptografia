from gerenciador import *
from gerarTokens import *
from pbkdf2 import *
from usuario import *
from criptografia import *
import base64

class Opcao():
    def __init__(self):
        pass
    
    def iniciar(self):
            sair = False
            while(not sair):
                print("Para adicionar um novo usuario digite 1\n",
              "Para cifrar uma mensagem digite 2\n",
              "Para decifrar uma mensagem digite 3\n",
              "Para sair digite 4\n"
              )
                opcao = int(input("Digite uma opção: "))
                if(opcao == 1):
                    self.opt1()
                elif(opcao == 2):
                    self.opt2()
                elif(opcao == 3):
                    self.opt3()
                elif(opcao == 4):
                    sair = True
                    print("Muito obrigado por utilizar o programa! Até a proxima!")
    
    
    def opt1(self):
        gerenciador = Gerenciador()
        pbkdf = GeradorChave()
        token = GeradorRandom()       
        if(gerenciador.arquivoCriado("./chaves/gerenciador.txt")):
            chave = self.opt4(gerenciador)
        else:
            chave = self.chaveGerenciador(gerenciador) 
            
        print("Voce deseja alterar o numero de iterações da chave(100.000) e o tamanho padrão(32)?")
        op = int(input(" Digite:\n 1 para sim \n 0 para não "))
        if(op == 1):
            # Inputs
            nome = str(input("Digite o nome de usuario: "))
            senha = input("Digite a sua senha: ")
            inter = int(input("Numero de iterações: "))
            tam = int(input("Tamanho da chave: "))
            # Criação da chave usando PBKDF2 e dos parametros do usuario
            salt = token.gerarSalt()
            nonce = token.gerarNonce()
            iv = token.gerarIV()
            aad = token.gerarAAD()
            chaveUser = pbkdf.crypt(senha, salt,tam, inter)
        elif(op == 0):
            # Inputs
            nome = str(input("Digite o nome de usuario: "))
            senha = str(input("Digite a sua senha: "))
            # Criação da chave usando PBKDF2 e dos parametros do usuario
            salt = token.gerarSalt()
            nonce = token.gerarNonce()
            iv = token.gerarIV()
            aad = token.gerarAAD()
            chaveUser = pbkdf.crypt(senha, salt)   
            
        # Passando tudo para string para colocar no gerenciador
        chaveUser = self.byteToStr(chaveUser)
        nonce = self.byteToStr(nonce)
        iv = self.byteToStr(iv)
        salt = self.byteToStr(salt)   
        aad = self.byteToStr(aad)
                
        #Criação do usuario e escrever os dados no arquivo gerenciador 
        gerenciador.wrt(nome, chaveUser, nonce, iv, salt, aad)        
        gerenciador.fileCrypt(chave)

    def opt2(self):
        gerenciador = Gerenciador()        
        if(gerenciador.arquivoCriado("./chaves/gerenciador.txt")):
            # Decifrando o arquivo gerenciador
            chave = self.opt4(gerenciador)            
            # Passando o seu nome e o nome da pessoa que vai receber a mensagem e a mensagem
            nomeOrigem = str(input("Digite o seu nome de usuario: "))
            nomeDestino = str(input("Digite o nome de usuario que você deseja enviar uma mensagem: "))
            linha = gerenciador.acharNome(nomeDestino,"./chaves/gerenciador.txt")
            if(linha):
                chaveUser = self.strToByte(gerenciador.acharParametros(linha, "chave:")) 
                nonce = self.strToByte(gerenciador.acharParametros(linha, "nonce:")) 
                aad = self.strToByte(gerenciador.acharParametros(linha, "aad:"))
                iv = self.strToByte(gerenciador.acharParametros(linha, "iv:"))                
                usuario = Usuario()
                cript = Criptografia()
                msg = str(input("Digite a sua mensagem: "))
                print("ATENÇÃO NESTA VERSÃO APENAS O MODO GCM ESTÁ FUNCIONANDO,FAVOR SELECIONAR OPÇÃO 1")               
                print("Você pode escolher um algoritmo de criptografia:\n",
                      "Para AES em modo GCM digite 1\n",
                      "Para AES em modo CBC digite 2\n",
                      "Para AES em modo CTR digite 3\n")
                opcao = int(input("Digite uma opção: "))
                if(opcao == 1):
                    msgc = cript.encryptGCM(msg, chaveUser, nonce)
                    msgc = self.byteToStr(msgc)
                    gerenciador.wrtMSG(nomeDestino,nomeOrigem, msgc)               
                    usuario.enviarMSG(msgc, nomeDestino)
                elif(opcao == 2):                                      
                    msgc = cript.encryptCBC(chaveUser,iv,msg)
                    msgc = self.byteToStr(msgc)                
                    usuario.enviarMSG(msgc, nomeDestino)
                elif(opcao == 3):
                    msgc = cript.encryptCTR(chaveUser,nonce,msg)
                    msgc = self.byteToStr(msgc)                
                    usuario.enviarMSG(msgc, nomeDestino) 
                else:
                    print("Digite uma opção valida!")                
            else:
                print("Usuario não encontrado na base de dados!")
        else:
            print("\nCadastre um usuario antes de utilizar!!\n")
        gerenciador.fileCrypt(chave)
         
    def opt3(self):
        gerenciador = Gerenciador()        
        if(gerenciador.arquivoCriado("./mensagem/mensagem.txt")):
            # Decifrando o arquivo gerenciador
            chave = self.opt4(gerenciador)            
            # Passando o seu nome e o nome da pessoa que vai receber a mensagem e a mensagem
            nome = str(input("Digite o seu nome de usuario: "))
            linha = gerenciador.acharNome(nome,"./chaves/gerenciador.txt")
            linhaMsg= gerenciador.acharNome(nome,"./mensagem/mensagem.txt")
            if(linha and linhaMsg):
                chaveUser = self.strToByte(gerenciador.acharParametros(linha, "chave:")) 
                nonce = self.strToByte(gerenciador.acharParametros(linha, "nonce:")) 
                aad = self.strToByte(gerenciador.acharParametros(linha, "aad:"))
                iv = self.strToByte(gerenciador.acharParametros(linha, "iv:")) 
                msg = input("Copie e cole a mensagem: ")             
                msg= self.strToByte(msg)
                nomeOrigem = gerenciador.acharParametros(linhaMsg,"de")                
                usuario = Usuario()
                cript = Criptografia()                
                print("ATENÇÃO NESTA VERSÃO APENAS O MODO GCM ESTÁ FUNCIONANDO,FAVOR SELECIONAR OPÇÃO 1")               
                print("Você pode escolher um algoritmo de criptografia:\n",
                      "Para AES em modo GCM digite 1\n",
                      "Para AES em modo CBC digite 2\n",
                      "Para AES em modo CTR digite 3\n")
                opcao = int(input("Digite uma opção: "))
                if(opcao == 1):
                    msgc = cript.decryptGCM(chaveUser,msg,nonce).decode()
                    usuario.receberMSG(msgc, nomeOrigem)
                elif(opcao == 2):                                      
                    msgc = cript.encryptCBC(chaveUser,iv,msg)
                    msgc = self.byteToStr(msgc)                
                    usuario.receberMSG(msgc, nomeOrigem)
                elif(opcao == 3):
                    msgc = cript.encryptCTR(chaveUser,nonce,msg)
                    msgc = self.byteToStr(msgc)                
                    usuario.receberMSG(msgc, nomeOrigem)
                else:
                    print("Digite uma opção valida!")                
            else:
                print("Usuario e/ou parametros não encontrados na base de dados!")
        else:
            print("\nNão há mensagens ainda!!!\n")
        gerenciador.fileCrypt(chave)
        
    def opt4(self, gerenciador):
        chave = input("Digite a chave mestre para decifrar o arquivo do gerenciador: ")
        chave = bytes(chave, 'utf-8')
        gerenciador.fileDecrypt(chave)
        return chave
   
    def chaveGerenciador(self, gerenciador):
        chave = gerenciador.chaveCrypt()        
        chavePrint = chave.decode()
        print("Guarde sua chave com muito cuidado, caso à perca não será possivel decifrar o arquivo: ",chavePrint)
        return chave  
        

    def byteToStr(self,param):
        param = base64.b64encode(param).decode()
        return param
    
    def strToByte(self,param):
        param = base64.b64decode(bytes(param, 'utf-8'))
        return param
    
        