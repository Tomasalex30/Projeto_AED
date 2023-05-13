import tkinter as tk
import re
from tkinter import messagebox , ttk
from model.Cliente import * 
from model.Despesas import *
from model.Orcamento import *
from model.Lista.LinkedListDespesas import *
from model.Lista.LinkedListCliente import *
from model.Lista.LinkedListOrcamento import *
from model.Lista.Iterador import *

from tkcalendar import DateEntry  #fazer pip install tkcalendar no terminal


class View:
    def __init__(self, master):
        self.clientes_lista = LinkedListCliente()
        self.despesas_lista = LinkedListDespesas()
        self.orcamento_lista = LinkedListOrcamento()
        self.master = master
        self.master.geometry("500x300")
        self.master.title("Inicio")
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master)
        self.date_entry = tk.Entry(self.frame)
        self.frame.pack()
        self.frame_login()
        self.username = None
        self.password = None 
        self.orcamento = None
        self.gastos_mes = None
        self.count_orcamento = 0
    
    def frame_login(self):   #frame login 
        if self.frame:
            self.frame.destroy() #destruição da frame
        
        self.frame = tk.Frame(self.master) #recriação da frame
        self.frame.pack()

        self.master.geometry("500x300")
        self.master.title("Login")              
        self.master.resizable(False, False) #Não permite ampliar
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="USERNAME")
        self.label.grid(row=0, column=0)   #label password
        self.nome_entry = tk.Entry(self.frame)  #Entrada para escrever username- pag. inicial
        self.nome_entry.grid(row=1, column=0, pady=5)   

        self.password_label = tk.Label(self.frame, text="PASSWORD")
        self.password_label.grid(row=2, column=0)  #label password
        validar_password = (self.master.register(self.tamanho_password), '%P')
        self.password_entry = tk.Entry(self.frame, show='*', validate='key', validatecommand=validar_password, width=16)  #Entrada para escrever password- pag. inicial
        self.password_entry.grid(row=3, column=0)

        self.voltar_button = tk.Button(self.frame, text="VER/OCULTAR", command=self.ver_login)
        self.voltar_button.grid(row=3, column=1) #Botao ver/ocultar password - pag inicial

        self.login_button = tk.Button(self.frame, text="LOGIN", command=self.login)
        self.login_button.grid(row=4, column=0) #Botao Login - pag inicial
        
        self.register_button = tk.Button(self.frame, text="REGISTER", command=self.frame_registo) #ver nova frame
        self.register_button.grid(row=5, column=0)  #Botao Registar - pag inicial

        self.quit_button = tk.Button(self.frame, text="SAIR", command=exit)
        self.quit_button.grid(row=6, column=0)  #Botao Sair do programa - pag inicial

    def login(self):
            username_login = self.nome_entry.get()
            password_login = self.password_entry.get()
            
            verificacao_login = True
            if len(username_login)==0 :
                messagebox.showinfo("Erro", "Complete o nome")#teste de nome completo
                verificacao_login = False

            if len(password_login)==0 :
                messagebox.showinfo("Erro", "Complete a password")# teste de password completa
                verificacao_login = False

            if len(password_login) > 0 and len(password_login) < 8:
                messagebox.showinfo("Erro", "Password Pequena") # teste de passworde com poucos caracteres
                verificacao_login = False
            
            if verificacao_login == False:
                if self.frame:                         #reabrir o frame login 
                    self.frame.destroy()
                    self.frame_login()

            if verificacao_login == True:                                  
                count = 0
                for cliente in self.clientes_lista:    #verificacao basica de login passada
                    if cliente != None:
                        count += 1
                if count == 0:
                    messagebox.showinfo("Erro", "Não existem Utilizadores Registados")  #verifica o caso de n haver utilizadores resgistados
                    verificacao_login = False
                
                if verificacao_login == True:
                    cliente_encontrado = None  # cardenciais de login testadas para encontrar um cliente resgistado a quais estas correspondam
                    for cliente in self.clientes_lista:
                        if cliente.get_nome() == username_login and cliente.get_password() == password_login:
                            cliente_encontrado = cliente
                            password_encontrada = password_login
                            break
                    
                    if cliente_encontrado:
                        self.username = username_login
                        self.password = password_login
                        messagebox.showinfo("Sucesso", "Login bem-sucedido")

                        if self.frame:                       
                            self.frame.destroy()    #Login efetuado- Open Menu frame
                            self.frame_menu()
            
                    else:
                        messagebox.showinfo("Erro", "Credenciais inválidas")
                        if self.frame:
                            self.frame.destroy()    #Login falhado-Reopen login frame
                            self.frame_login()

    def ver_login(self): #ver/ocultar pw login
        if self.password_entry["show"] == "*":
            self.password_entry["show"] = "" #revelar password
        else:                                                  
            self.password_entry["show"] ="*" #esconder password

    def frame_registo(self):      #frame registo
        if self.frame:
            self.frame.destroy()    #Destruicao da frame
        
        self.frame = tk.Frame(self.master)
        self.frame.pack()                   #Recriacao da frame

        self.master.geometry("500x300")
        self.master.title("Registo")
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master)
        self.frame.pack()                       #Dimensoes da frame
 
        self.nome_label = tk.Label(self.frame, text="USERNAME")
        self.nome_label.grid(row=0, column=0)   
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=1, column=0, pady=5)   #Entrada para username- pag. registo

        self.password_label = tk.Label(self.frame, text="PASSWORD")
        self.password_label.grid(row=2, column=0)  
        validar_password = (self.master.register(self.tamanho_password), '%P')
        self.password_entry = tk.Entry(self.frame, show='*', validate='key', validatecommand=validar_password, width=16)
        self.password_entry.grid(row=3, column=0)          #Entrada para password - pag. registo

        self.password_label_2 = tk.Label(self.frame, text="REPETIR PASSWORD")
        self.password_label_2.grid(row=4, column=0)   
        validar_password = (self.master.register(self.tamanho_password), '%P')
        self.password_entry_2 = tk.Entry(self.frame, show='*', validate='key', validatecommand=validar_password, width=16)
        self.password_entry_2.grid(row=5, column=0)              # Entrada para repetir password - pag.registo

        self.info_password = tk.Label(self.frame, text="A palavra passe deve ter no máximo 16 carácteres")
        self.info_password.grid(row=10, column=0)

        self.ver_ocultar_button = tk.Button(self.frame, text="VER/OCULTAR", command=self.ver_registo)
        self.ver_ocultar_button.grid(row=3, column=1)      #Botão para ver/ocultar a password- pag. registo
         
        self.nif_label = tk.Label(self.frame, text="NIF")
        self.nif_label.grid(row=6, column=0)
        def validar_nif(entrada):                                 
            if entrada.isdigit() and len(entrada) <= 9:              #Funcao de funcionamento do NIF
                return True
            else:
                return False
        validacao_nif = self.master.register(validar_nif)
        self.nif_entry = tk.Entry(self.frame, validate='key', validatecommand=(validacao_nif, '%P'), width=9)
        self.nif_entry.grid(row=7, column=0, pady=5)  #Entrada para o NIF - pag registo
        
        self.login_button = tk.Button(self.frame, text="REGISTAR", command=self.registar)
        self.login_button.grid(row=8, column=0) #Botao para registar - pag registo
        
        self.voltar_button = tk.Button(self.frame, text="VOLTAR", command=self.frame_login)
        self.voltar_button.grid(row=9, column=0)    #Botao para voltar para a pag inicial - pag. registo
    
    def registar(self): #função registar                                              
            nome_registo = self.nome_entry.get()
            password_registo = self.password_entry.get()             
            password_registo_2 = self.password_entry_2.get()
            nif = self.nif_entry.get()
            
            verificacao_registo = True
            if len(nome_registo)==0 : 
                messagebox.showinfo("Erro", "Complete o nome")     #Condicoes para verificacao de dados na pag de registo 
                verificacao_registo = False

            if len(password_registo)==0  :
                messagebox.showinfo("Erro", "Complete a password")  #Condicoes para verificacao de dados na pag de registo
                verificacao_registo = False

            if len(password_registo_2)==0  :
                messagebox.showinfo("Erro", "Complete a confirmação de password")      #Condicoes para verificacao de dados na pag de registo 
                verificacao_registo = False

            if password_registo != password_registo_2 and len(password_registo_2)>0 and len(password_registo)>0:    #Condicoes para verificacao de dados na pag de registo 
                messagebox.showinfo("Erro", "Passwords diferentes")
                verificacao_registo = False

            if len(nif)==0:
                messagebox.showinfo("Erro", "Complete o NIF")        #Condicoes para verificacao de dados na pag de registo 
                verificacao_registo = False

            if len(password_registo) > 0 and len(password_registo) < 8:
                messagebox.showinfo("Erro", "Password Pequena") 
                verificacao_registo = False

            if len(nif) < 9:                                           #Condicoes para verificacao de dados na pag de registo 
                if len(nif) == 0:
                    pass
                else:
                    messagebox.showinfo("Erro", "NIF Pequeno")
                    verificacao_registo = False

            for cliente in self.clientes_lista:
                if cliente.get_nome() == nome_registo:
                    messagebox.showinfo("Erro", "Nome de registo já existente")     #Condicoes para verificacao de dados na pag de registo 
                    verificacao_registo = False
                    break                                                     

            for cliente in self.clientes_lista:
                if cliente.get_nif() == nif:
                    messagebox.showinfo("Erro", "NIF já existente")     #Condicoes para verificacao de dados na pag de registo
                    verificacao_registo = False
                    break                                                

            if verificacao_registo == False:
                if self.frame:
                    self.frame.destroy()
                    self.frame_registo()

            if verificacao_registo == True:
                cliente = Cliente(nome_registo,password_registo,nif)
                self.clientes_lista.append_cliente(cliente)
                self.clientes_lista.print_list_cliente()
                messagebox.showinfo("Sucesso", "Registo bem-sucedido")   #Condicao caso todos os dados de registo estejam corretos
                    
                if self.frame:
                    self.frame.destroy()              #Destruicao da frame
                    self.frame_login()                #Reencaminhamento de volta para a frame inicial caso os dados de registo estejam corretos
            
    def ver_registo(self): #função para caracteres escondidos
        if self.password_entry["show"] == "*" and self.password_entry_2["show"] == "*" : #verifica se ambas estao escondidas
            self.password_entry["show"] = "" #revelar password 1
            self.password_entry_2["show"] = "" #revelar password 2
        else :
            self.password_entry["show"] ="*" #esconder password 1
            self.password_entry_2["show"] = "*" #esconder password 2

    def frame_menu(self): #frame menu

        if self.frame:
            self.frame.destroy() #destruição frame
        
        self.frame = tk.Frame(self.master) #recriação frame
        self.frame.pack()

        self.master.geometry("500x300")
        self.master.title("Menu")           #delimitador frame
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        #VER O GRID DEPOIS
        self.adicionar_depesas = tk.Button( self.frame ,text = "Adicionar despesas: ", command=self.frame_adicionar_despesas) #botao adicionar despesas
        self.adicionar_depesas.grid(row=3 , column=1,)#not working
        
        self.ver_depesas = tk.Button( self.frame , text = "Ver despesas: ", command = self.frame_ver_despesa) #botao ver despesas
        self.ver_depesas.grid(row=5 , column=1,)#not working
        
        self.orcamento = tk.Button(self.frame ,  text= "Definir orçamento mensal:", command= self.frame_ver_orcamento) #botao orçamento
        self.orcamento.grid(row=7 , column=1)#not working

        self.sign_out = tk.Button(self.frame ,  text= "SIGN OUT", command= self.frame_login) #botao voltar
        self.sign_out.grid(row=9 , column=1)#not working
    
    def frame_adicionar_despesas(self): #frame add despesas
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(self.master) #recriação da frame
        self.frame.pack()

        self.master.geometry("500x300")
        self.master.title("Adicionar Despesas")     #delimitador frame
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Categoria da despesa") #label categoria
        self.label.grid(row=0, column=0)

        self.combo = ttk.Combobox( #biblioteca para metodo de seleção
            self.frame,
            state="readonly",
            values=["Selecione a Categoria", "a", "b", "c", "d"]  #valores da categoria a escolher
        )

        self.combo.grid(row=0, column=1)
        self.combo.current(0) #cabeçalho do combo

        self.descricao_label = ttk.Label(self.frame, text="Descrição") #label descricao
        self.descricao_label.grid(row=1, column=0)
        self.descricao_entry = tk.Entry(self.frame) #entry descrição
        self.descricao_entry.grid(row=1, column=1, pady=5)

        self.valor_label = ttk.Label(self.frame, text="Valor da despesa") #entry label
        self.valor_label.grid(row=2, column=0)
        self.valor_entry = tk.Entry(self.frame) #entry valor
        self.valor_entry.grid(row=2, column=1, pady=5)
        valor_numerico = self.master.register(self.verificar_numerico) #verificacao para apenas escrever numerico e .
        self.valor_entry.config(validate="key", validatecommand=(valor_numerico, "%P"))

        self.data_label = ttk.Label(self.frame, text="Data da despesa") #label data
        self.data_label.grid(row=3, column=0)
        self.data_entry = DateEntry(self.frame) #entry data
        self.data_entry.grid(row=3, column=1, pady=5)

        self.adicionar_button = tk.Button(self.frame, text="ADICIONAR", command=self.adicionar_despesas) #botao adicionar
        self.adicionar_button.grid(row=4, column=0)
        
        self.voltar_button = tk.Button(self.frame, text="VOLTAR", command=self.frame_menu) #botao voltar
        self.voltar_button.grid(row=4, column=1)
    
    def adicionar_despesas(self): #função adicionar despesas
        categoria = self.combo.get() #valor entry categoria
        descricao = self.descricao_entry.get() #valor entry descrição
        valor = self.valor_entry.get() #valor entry valor
        data = self.data_entry.get() #valor entry data

        verificacao_despesas = True
        if self.orcamento == None:
            messagebox.showinfo("Erro", "Não existe Orçamento") #verificacao mensagem longa 
            verificacao_despesas = False
        if len(descricao) > 160:
            messagebox.showinfo("Erro", "Descrição demasiado longa!") #verificacao mensagem longa 
            verificacao_despesas = False
        if len(descricao) == 0:
            messagebox.showinfo("Erro", "Complete a descrição")
            verificacao_despesas = False
        if len(valor) == 0:
            messagebox.showinfo("Erro", "Defina o valor")
            verificacao_despesas = False
        if categoria == "Selecione a Categoria": #verificacao categoria invalida
            messagebox.showinfo("Erro", "Categoria Inválida")
            verificacao_despesas = False

        if verificacao_despesas == True:
            valor_final_verificacao = float(valor)
            despesa = Despesas(categoria, descricao, valor_final_verificacao, data) #adicionar as despesas na classe Despesa
            self.despesas_lista.append_despesas(despesa) #adicionar as despesas na linked list
            messagebox.showinfo("Sucesso", "Categoria adicionada com sucesso")
            
            username_atual = self.username
            password_atual = self.password
            self.clientes_lista.cliente_logado(username_atual, password_atual)
            self.clientes_lista.adicionar_despesa_cliente_logado(categoria, descricao, valor, data)
            self.clientes_lista.print_list_cliente_despesas_orcamento()

            if self.frame:
                self.frame.destroy()    #destruir a frame
                self.frame_menu()       #aceder a frame anterior
        
    def frame_ver_despesa(self):    #frame ver despesas
        if self.frame:              
            self.frame.destroy()    #destruição da frame
        
        self.frame = tk.Frame(self.master) #recriação da frame
        self.frame.pack()

        self.master.geometry("500x300")
        self.master.title("Vizualizar Despesas")
        self.master.resizable(False, False)     #delimitadores da frame
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.name_label = tk.Button(self.frame, text="VOLTAR", command=self.frame_menu) #botao voltar
        self.name_label.grid(row=0, column=0)    
    
    def frame_ver_orcamento(self): #frame ver orçamento
        if self.frame:
            self.frame.destroy()    #eliminar a frame
        
        self.frame = tk.Frame(self.master)  #recriar a frame
        self.frame.pack()

        self.master.geometry("500x300")
        self.master.title("Orçamento")
        self.master.resizable(False, False)     #delimitadores de frame 
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.gastos_label = ttk.Label(self.frame, text="Máximo de gastos para o mês") #gastos label
        self.gastos_label.grid(row=0, column=0)
        self.gastos_entry = tk.Entry(self.frame) #entry gastos
        self.gastos_entry.grid(row=1, column=0, pady=5)
        valor_numerico_gastos = self.master.register(self.verificar_numerico) #verificacao para apenas escrever numerico e .
        self.gastos_entry.config(validate="key", validatecommand=(valor_numerico_gastos, "%P"))    

        self.orcamento_label = ttk.Label(self.frame, text="Orçamento") #orcamento label
        self.orcamento_label.grid(row=2, column=0)
        self.orcamento_entry = tk.Entry(self.frame) #orcamento valor
        self.orcamento_entry.grid(row=3, column=0, pady=5)
        valor_numerico_orcamento = self.master.register(self.verificar_numerico) #verificacao para apenas escrever numerico e .
        self.orcamento_entry.config(validate="key", validatecommand=(valor_numerico_orcamento, "%P"))  
        
        self.definir_orc_button = tk.Button(self.frame, text="DEFINIR", command=self.definir_orcamento) #botao para definir orçamento
        self.definir_orc_button.grid(row=4, column=0)

        self.voltar_button = tk.Button(self.frame, text="VOLTAR", command=self.frame_menu) #botao voltar
        self.voltar_button.grid(row=5, column=0)

    def definir_orcamento(self):
        gastos_mes = self.gastos_entry.get()
        orcamento = self.orcamento_entry.get()

        verificacao_orcamento = True
        if gastos_mes > orcamento:
            messagebox.showinfo("Erro", "Gastos para o mês superiores ao orçamento")
            verificacao_orcamento = False
        if self.count_orcamento > 0:
            messagebox.showinfo("Erro", "O orçamento já foi definido")
            verificacao_orcamento = False
        if len(gastos_mes) == 0:
            messagebox.showinfo("Erro", "Defina os gastos para o mês")
            verificacao_orcamento = False
        if len(orcamento) == 0:
            messagebox.showinfo("Erro", "Defina o orçamento")
            verificacao_orcamento = False
    
        if verificacao_orcamento == True:
            gastos_mes_final_verificacao = float(gastos_mes)
            orcamento_final_verificacao = float(orcamento)
            self.count_orcamento += 1
            orcamento_final = Orcamento(gastos_mes_final_verificacao, orcamento_final_verificacao, self.count_orcamento) #adicionar as despesas na classe Despesa
            self.despesas_lista.append_orcamento(orcamento_final) #adicionar as despesas na linked list
            messagebox.showinfo("Sucesso", "Conjunto Orçamento feito com Sucesso")
            
            username_atual = self.username
            password_atual = self.password
            self.clientes_lista.cliente_logado(username_atual, password_atual)
            self.clientes_lista.adicionar_orcamento_cliente_logado(gastos_mes, orcamento, self.count_orcamento)
            self.clientes_lista.print_list_cliente_despesas_orcamento()

            if self.frame:
                self.frame.destroy()    #destruir a frame
                self.frame_menu()  
    
    def tamanho_password(self, tamanho):    #função que serve para verificar o tamaho da password
        if len(tamanho) <= 16 :
            return True
        else:
            self.master.bell() 
            return False
        
    def verificar_numerico(self, valor): #função para apenas escrever numerico ou .
        return re.match(r"^\d*\.?\d*$", valor) is not None #biblioteca para verificar se o valor escrito é numerico ou um .
    