import tkinter as tk
import re
import random
import datetime
import locale
import json
import matplotlib.pyplot as plt #fazer pip install matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        self.load_lists_from_json()
        self.master.geometry("500x300")
        self.master.title("Inicio")
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master)
        self.date_entry = tk.Entry(self.frame)
        self.frame.pack()
        self.frame_login()
        self.tree = None
        self.username = None
        self.password = None 
        self.orcamento = None
        self.gastos_mes = None
        self.orcamento_final_verificacao = None
        self.valor_final_verificacao = None
        self.gastos_mes_final_verificacao = None
        self.count_orcamento = 0
    
    def frame_login(self):   #frame login 
        
        if self.frame:
            self.frame.destroy() #destruição da frame   

        self.master.geometry("455x330")
        self.master.title("Login")              
        self.master.resizable(False, False) #Não permite ampliar
        self.frame = tk.Frame(self.master, bg="#0076a3")
        self.frame.pack(fill=tk.BOTH , expand=True)
        self.invisivel = tk.Label(self.frame, text="                                       ", bg="#0076a3")#Para ficar direito com o resto
        self.invisivel.grid(row=0,column=0)

        frame = "imagens/UAL_frame.png"
        self.logo = tk.PhotoImage(file=frame)
        self.logo = self.logo.subsample(3)
        self.logo_label = tk.Label(self.frame, image= self.logo)
        self.logo_label.grid(row=0, column=3)
        
        self.label = tk.Label(self.frame, text="USERNAME",font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.label.grid(row=1, column=1)   #label password
        self.nome_entry = tk.Entry(self.frame)  #Entrada para escrever username- pag. inicial
        self.nome_entry.grid(row=2, column=1, pady=5)   

        self.password_label = tk.Label(self.frame, text="PASSWORD",font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.password_label.grid(row=3, column=1)  #label password
        validar_password = (self.master.register(self.tamanho_password), '%P')
        self.password_entry = tk.Entry(self.frame, show='*', validate='key', validatecommand=validar_password, width=16)  #Entrada para escrever password- pag. inicial
        self.password_entry.grid(row=4, column=1)

        self.voltar_button = tk.Button(self.frame, text="VER/OCULTAR",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.ver_login)
        self.voltar_button.grid(row=4, column=2) #Botao ver/ocultar password - pag inicial

        self.login_button = tk.Button(self.frame, text="LOGIN",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.login)
        self.login_button.grid(row=5, column=1) #Botao Login - pag inicial
        
        self.register_button = tk.Button(self.frame, text="REGISTAR",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.frame_registo) #ver nova frame
        self.register_button.grid(row=6, column=1)  #Botao Registar - pag inicial

        self.quit_button = tk.Button(self.frame, text="SAIR",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.save_lists_to_json)
        self.quit_button.grid(row=7, column=1)  #Botao Sair do programa - pag inicial

    def login(self):
            username_login = self.nome_entry.get()      #username logado no momento
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
                    
                    if cliente_encontrado: #se o login for feito corretamente
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

        
        self.master.geometry("420x320")
        self.master.title("Registo")
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master, bg="#0076a3")
        self.frame.pack(fill=tk.BOTH , expand = True)                       #Dimensoes da frame
        self.invisivel = tk.Label(self.frame,text="         ", bg="#0076a3")#Para ficar direito com o resto
        self.invisivel.grid(row=0,column=0)

        self.nome_label = tk.Label(self.frame, text="USERNAME", font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.nome_label.grid(row=1, column=1)   
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=2, column=1, pady=5)   #Entrada para username- pag. registo

        self.password_label = tk.Label(self.frame, text="PASSWORD", font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.password_label.grid(row=3, column=1)  
        validar_password = (self.master.register(self.tamanho_password), '%P')
        self.password_entry = tk.Entry(self.frame, show='*', validate='key', validatecommand=validar_password, width=16)
        self.password_entry.grid(row=4, column=1)          #Entrada para password - pag. registo

        self.password_label_2 = tk.Label(self.frame, text="REPETIR PASSWORD", font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.password_label_2.grid(row=5, column=1)   
        validar_password = (self.master.register(self.tamanho_password), '%P')
        self.password_entry_2 = tk.Entry(self.frame, show='*', validate='key', validatecommand=validar_password, width=16)
        self.password_entry_2.grid(row=6, column=1)              # Entrada para repetir password - pag.registo

        self.info_password = tk.Label(self.frame, text="A palavra passe deve ter no máximo 16 carácteres",font=("Arial",8), fg="#ffffff", bg="#0076a3")
        self.info_password.grid(row=11, column=1)

        self.ver_ocultar_button = tk.Button(self.frame, text="VER/OCULTAR", font=("Arial",10), fg="#000000", bg="#ffffff", command=self.ver_registo)
        self.ver_ocultar_button.grid(row=4, column=2)      #Botão para ver/ocultar a password- pag. registo
         
        self.nif_label = tk.Label(self.frame, text="NIF", font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.nif_label.grid(row=7, column=1)
        def validar_nif(entrada):                                 
            if entrada.isdigit() and len(entrada) <= 9:              #Funcao de funcionamento do NIF
                return True
            else:
                return False
        validacao_nif = self.master.register(validar_nif)
        self.nif_entry = tk.Entry(self.frame, validate='key', validatecommand=(validacao_nif, '%P'), width=9)
        self.nif_entry.grid(row=8, column=1, pady=5)  #Entrada para o NIF - pag registo
        
        self.login_button = tk.Button(self.frame, text="REGISTAR",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.registar)
        self.login_button.grid(row=9, column=1) #Botao para registar - pag registo
        
        self.voltar_button = tk.Button(self.frame, text="VOLTAR",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.frame_login)
        self.voltar_button.grid(row=10, column=1)    #Botao para voltar para a pag inicial - pag. registo
   
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
                #self.clientes_lista.print_list_cliente()  #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
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

        self.master.geometry("330x320")
        self.master.title("Menu")           #delimitador frame
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master, bg="#0076a3")
        self.frame.pack(fill=tk.BOTH , expand = True)
        
        self.invisivel = tk.Label(self.frame,text="         ", bg="#0076a3")#Para ficar direito com o resto
        self.invisivel.grid(row=0,column=0)
        frame_1 = "imagens/despesas.png"
        self.logo_despesas = tk.PhotoImage(file=frame_1)
        self.logo_despesas = self.logo_despesas.subsample(3)
        self.logo_label = tk.Label(self.frame, image= self.logo_despesas, bg="#0076a3")
        self.logo_label.grid(row=3, column=3)
        self.adicionar_depesas = tk.Button( self.frame ,text = "Adicionar despesas: ",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.frame_adicionar_despesas) #botao adicionar despesas
        self.adicionar_depesas.grid(row=3 , column=1)
        
        frame_2 = "imagens/ver_despesas.png"
        self.logo_ver_despesas = tk.PhotoImage(file=frame_2)
        self.logo_ver_despesas = self.logo_ver_despesas.subsample(3)
        self.logo_label = tk.Label(self.frame, image= self.logo_ver_despesas, bg="#0076a3")
        self.logo_label.grid(row=5, column=3)
        self.ver_depesas = tk.Button( self.frame , text = "Ver despesas: ",font=("Arial",10), fg="#000000", bg="#ffffff", command = self.frame_ver_despesa) #botao ver despesas
        self.ver_depesas.grid(row=5 , column=1,)
        
        frame_3 = "imagens/orcamento.png"
        self.logo_orcamento = tk.PhotoImage(file=frame_3)
        self.logo_orcamento = self.logo_orcamento.subsample(3)
        self.logo_label = tk.Label(self.frame, image= self.logo_orcamento, bg="#0076a3")
        self.logo_label.grid(row=7, column=3)
        self.orcamento = tk.Button(self.frame ,  text= "Definir orçamento mensal:",font=("Arial",10), fg="#000000", bg="#ffffff", command= self.frame_definir_orcamento) #botao definir orçamento
        self.orcamento.grid(row=7 , column=1)

        self.sign_out = tk.Button(self.frame ,  text= "SIGN OUT",font=("Arial",10), fg="#000000", bg="#ffffff", command= self.frame_login) #botao voltar
        self.sign_out.grid(row=9 , column=1)

    def frame_adicionar_despesas(self):
        if self.frame:
            self.frame.destroy()

        self.master.geometry("700x250")
        self.master.title("Adicionar Despesas")     #delimitador frame
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master, bg="#0076a3")
        self.frame.pack(fill=tk.BOTH , expand=True)
        self.invisivel = tk.Label(self.frame, text="                               ", bg="#0076a3")#Para ficar direito com o resto
        self.invisivel.grid(row=0,column=0)
        
        locale.setlocale(locale.LC_ALL, 'pt_PT')

        self.label = tk.Label(self.frame, text="Categoria da despesa",font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.label.grid(row=1, column=1)

        self.combo = ttk.Combobox(
            self.frame,
            state="readonly",
            values=["Selecione a Categoria", "Alimentação", "Lazer", "Habitação", "Transportes", "Outros"]
        )

        self.combo.grid(row=1, column=2)
        self.combo.current(0)

        self.descricao_label = tk.Label(self.frame, text="Descrição",font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.descricao_label.grid(row=2, column=1)
        self.descricao_entry = tk.Entry(self.frame)
        self.descricao_entry.grid(row=2, column=2, pady=5)

        self.valor_label = tk.Label(self.frame, text="Valor da despesa",font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.valor_label.grid(row=3, column=1)
        self.valor_entry = tk.Entry(self.frame)
        self.valor_entry.grid(row=3, column=2, pady=5)
        valor_numerico = self.master.register(self.verificar_numerico)
        self.valor_entry.config(validate="key", validatecommand=(valor_numerico, "%P"))

        self.data_label = tk.Label(self.frame, text="Data da despesa",font=("Arial"), fg="#ffffff", bg="#0076a3")
        self.data_label.grid(row=4, column=1)
        self.data_entry = DateEntry(self.frame, locale='pt_PT', date_pattern="dd/mm/yyyy")
        self.data_entry.grid(row=4, column=2, pady=5)

        self.adicionar_button = tk.Button(self.frame, text="ADICIONAR",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.adicionar_despesas)
        self.adicionar_button.grid(row=5, column=1)
        
        self.adicionar_button = tk.Button(self.frame, text="SUGESTÕES",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.sugestoes)
        self.adicionar_button.grid(row=5, column=2)

        self.voltar_button = tk.Button(self.frame, text="VOLTAR",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.frame_menu)
        self.voltar_button.grid(row=5, column=3)

        gastos_mes_cliente_atual = float(self.clientes_lista.encontrar_gastos_mes_cliente_atual(self.clientes_lista))
        orcamento_cliente_atual = float(self.clientes_lista.encontrar_orcamento_cliente_atual(self.clientes_lista))
        total_despesas_cliente_atual = float(self.clientes_lista.calcular_total_despesas_cliente_atual(self.clientes_lista))
        resto_gastos_mes = gastos_mes_cliente_atual - total_despesas_cliente_atual
        resto_orcamento = orcamento_cliente_atual - total_despesas_cliente_atual
        
        if gastos_mes_cliente_atual != 0 or orcamento_cliente_atual != 0:
            self.nome_label = tk.Label(self.frame, text=f"Resta-lhe {resto_gastos_mes}€ de limite de gastos do mês",font=("Arial"), fg="#ffffff", bg="#0076a3")
            self.nome_label.grid(row=6, column=2)
            self.nome_label = tk.Label(self.frame, text=f"Resta-lhe {resto_orcamento}€ de orçamento",font=("Arial"), fg="#ffffff", bg="#0076a3")
            self.nome_label.grid(row=7, column=2)
        else:
            self.nome_label = tk.Label(self.frame, text=f"Não tem limite de gastos do mês", font=("Arial"), fg="#ffffff", bg="#0076a3")
            self.nome_label.grid(row=6, column=2)
            self.nome_label = tk.Label(self.frame, text=f"Não têm orçamento", font=("Arial"), fg="#ffffff", bg="#0076a3")
            self.nome_label.grid(row=7, column=2)
    
    def adicionar_despesas(self): #função adicionar despesas
        categoria = self.combo.get() #valor entry categoria
        descricao = self.descricao_entry.get() #valor entry descrição
        valor = self.valor_entry.get() #valor entry valor
        data = self.data_entry.get() #valor entry data

        verificacao_despesas_2 = None
        verificacao_despesas = True
        if len(descricao) > 160:
            messagebox.showinfo("Erro", "Descrição demasiado longa!") #verificacao mensagem longa 
            verificacao_despesas = False
        if len(descricao) == 0:
            messagebox.showinfo("Erro", "Complete a descrição") #verificação descrição
            verificacao_despesas = False
        if len(valor) == 0:
            messagebox.showinfo("Erro", "Defina o valor")
            verificacao_despesas = False
        if categoria == "Selecione a Categoria": #verificacao categoria invalida
            messagebox.showinfo("Erro", "Categoria Inválida")
            verificacao_despesas = False
            
        if verificacao_despesas == False:
            if self.frame:
                self.frame.destroy()                #destruir a frame
                self.frame_adicionar_despesas() 

        dia_selecionado = int(data.split("/")[0])
        mes_selecionado = int(data.split('/')[1])
        ano_selecionado = int(data.split("/")[2])
        # print("Dia selecionado:", dia_selecionado) 
        # print("Mês selecionado:", mes_selecionado)   #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
        # print("Ano selecionado:", ano_selecionado) 
        
        dia_atual = datetime.datetime.now().day
        mes_atual = datetime.datetime.now().month
        ano_atual = datetime.datetime.now().year
        # print("Dia atual:", dia_atual)
        # print("Mês atual:", mes_atual)    #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
        # print("Ano atual:", ano_atual)

        if verificacao_despesas == True:
            if mes_selecionado == mes_atual:
                if ano_selecionado == ano_atual:
                    if dia_selecionado <= dia_atual:  

                        if verificacao_despesas == True:
                            verificacao_despesas_2 = True
                            self.valor_final_verificacao = float(valor)
                            despesa = Despesas(categoria, descricao, self.valor_final_verificacao, data) #adicionar as despesas na classe Despesa
                            self.despesas_lista.append_despesas(despesa) #adicionar as despesas na linked list
                            
                            username_atual = self.username
                            password_atual = self.password
                            self.clientes_lista.cliente_logado(username_atual, password_atual) #Encontrar utilizador atual
                            
                            if self.clientes_lista.verificar_orcamento() != 1:
                                gastos_mes_cliente_atual = float(self.clientes_lista.encontrar_gastos_mes_cliente_atual(self.clientes_lista))         #
                                orcamento_cliente_atual = float(self.clientes_lista.encontrar_orcamento_cliente_atual(self.clientes_lista))           #
                                total_despesas_cliente_atual = float(self.clientes_lista.calcular_total_despesas_cliente_atual(self.clientes_lista))  # encontrar e defenir vareaveis do utilizador atual
                                resto_gastos_mes = gastos_mes_cliente_atual - total_despesas_cliente_atual                                            #
                                resto_orcamento = orcamento_cliente_atual - total_despesas_cliente_atual                                              #
                                
                                if resto_gastos_mes > 0:
                                    
                                    if self.valor_final_verificacao <= resto_orcamento:
                                        confirmacao_despesa = messagebox.askyesno("Confirmação", f"Deseja submeter a despesa de:\n\nCategoria: {categoria}\nDescrição: {descricao}\nValor: {self.valor_final_verificacao}€\nData: {data}") # verificacao de operacao
                                        
                                        if confirmacao_despesa == True:    
                                            
                                            if self.clientes_lista.adicionar_despesa_cliente_logado(categoria, descricao, valor, data) == 1:
                                                #self.clientes_lista.print_list_cliente_despesas_orcamento()#CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
                                                total_despesas_cliente_atual = float(self.clientes_lista.calcular_total_despesas_cliente_atual(self.clientes_lista))
                                                resto_gastos_mes = gastos_mes_cliente_atual - total_despesas_cliente_atual #gastos do mes atual
                                                resto_orcamento = orcamento_cliente_atual - total_despesas_cliente_atual #orcamento atual
                                                # print()
                                                # print("Total Despesas", total_despesas_cliente_atual)
                                                # print("Resto dos gastos do mes",resto_gastos_mes) #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
                                                # print("Resto orcamento", resto_orcamento)
                                                messagebox.showinfo("Sucesso", "Despesa criada com sucesso.")       # realizacao da operacao confirmada(adicionar despesa)
                                                
                                                if resto_gastos_mes < 0:
                                                    messagebox.showinfo("Aviso", "Excedeu os gastos do mês")     # Aviso excedeu gasto do mes
                                                elif resto_gastos_mes == 0:
                                                    messagebox.showinfo("Aviso", "Gastos do mês esgotados")      #Aviso gastos dos mes esgotado
                                                elif resto_gastos_mes <= gastos_mes_cliente_atual/10:
                                                    messagebox.showinfo("Aviso", f"Restam menos de 10% dos seus gastos do mes")      #Aviso 10% dos gastos do mes 
                                                elif resto_gastos_mes <= gastos_mes_cliente_atual/4:
                                                    messagebox.showinfo("Aviso", f"Restam menos de 25% dos seus gastos do mes")      #Aviso 25% dos gastos do mes 
                                                elif resto_gastos_mes <= gastos_mes_cliente_atual/2:
                                                    messagebox.showinfo("Aviso", f"Restam menos de 50% dos seus gastos do mes")      #Aviso 50% dos gastos do mes 
                                                elif resto_gastos_mes <= ((gastos_mes_cliente_atual*3)/4):
                                                    messagebox.showinfo("Aviso", f"Restam menos de 75% dos seus gastos do mês")      #Aviso 75% dos gastos do mes 

                                                if resto_orcamento == 0:
                                                    messagebox.showinfo("Aviso", "Orcamento esgotado")           #Aviso orcamento esgotado
                                                elif resto_orcamento <= orcamento_cliente_atual/10:
                                                    messagebox.showinfo("Aviso", f"Restam menos de 10% do seu orcamento")            #Aviso 10% do orocamento 
                                                elif resto_orcamento <= orcamento_cliente_atual/4:
                                                    messagebox.showinfo("Aviso", f"Restam menos de 25% do seu orcamento")            #Aviso 25% do orocamento 
                                                elif resto_orcamento <= orcamento_cliente_atual/2:
                                                    messagebox.showinfo("Aviso", f"Restam menos de 50% do seu orcamento")            #Aviso 50% do orocamento 
                                                elif resto_orcamento <= ((orcamento_cliente_atual*3)/4):
                                                    messagebox.showinfo("Aviso", f"Restam menos de 75% do seu orcamento")            #Aviso 75% do orocamento 
                                        else:
                                            verificacao_despesas_2 = False
                                    else:
                                        messagebox.showinfo("Erro", "Despesa maior que o orcamento")    # Erro logico de variaveis
                                        verificacao_despesas_2 = False
                                else:
                                    messagebox.showinfo("Erro", "Excedeu os gastos do mês")  #Erro excedeu os gastos do mes
                                    verificacao_despesas_2 = 1    
                            else:
                                messagebox.showinfo("Erro", "O cliente precisa criar um orçamento antes de adicionar despesas.")  #Erro falta de variavel importante
                                verificacao_despesas_2 = 1
                    else:
                        messagebox.showinfo("Erro", "A data da despesa não pode ser posterior à data atual.")    # Erro logico de variaveis
                        verificacao_despesas_2 = False  
                else:
                    messagebox.showinfo("Erro", "Apenas é possivel depositar despesas no ano atual")    # Erro logico de variaveis
                    verificacao_despesas_2 = False  
            else:
                messagebox.showinfo("Erro", "Apenas é possivel depositar despesas no mês atual")    # Erro logico de variaveis
                verificacao_despesas_2 = False        
        
        if verificacao_despesas_2 == False:
            if self.frame:
                self.frame.destroy()                #destruir a frame
                self.frame_adicionar_despesas()     #aceder a frame adicionar despesas
        
        if verificacao_despesas_2 == 1:
            if self.frame:
                self.frame.destroy()   #destruir a frame   
                self.frame_menu()      #aceder a frame anterior

        if verificacao_despesas_2 == True:
            if self.frame:
                self.frame.destroy()    #destruir a frame
                self.frame_menu()       #aceder a frame anterior
  
    def sugestoes(self):
        username_atual = self.username
        password_atual = self.password
        self.clientes_lista.cliente_logado(username_atual, password_atual)
        count_despesas = int(self.clientes_lista.calcular_count_despesas_cliente_atual(self.clientes_lista))
        
        lista_categorias = ["Alimentação", "Habitação", "Lazer", "Transportes", "Outros"]

        lista_alimentacao = ["Alimentação",
                             "Faça uma lista de compras antes de ir ao supermercado e siga-a rigorosamente. Isso ajuda a evitar compras impulsivas e desnecessárias.",
                             "Opte por frutas, legumes e verduras da estação, pois costumam ser mais baratos.",
                             "Prepare as suas refeições em casa sempre que possível. Comer fora ou pedir delivery geralmente é mais caro do que cozinhar em casa.",
                             "Se sobrar comida, não desperdice. Use as sobras para criar novas refeições, como sopas, saladas, sanduíches ou omeletes."
                             ]
        
        lista_habitacao = ["Habitação",
                           "Desligue luzes e aparelhos eletrônicos quando não estiver a usar, utilize lâmpadas econômicas, aproveite a luz natural durante o dia e evite deixar aparelhos em standby.",
                           "Tome banhos mais curtos, conserte fugas de água, utilize a máquina de lavar roupas e louças apenas quando estiver com a carga completa e aproveite água da chuva para regar plantas.",
                           "Avalie se você realmente utiliza todos os canais e serviços contratados. Considere reduzir o pacote ou migrar para opções mais econômicas.",
                           "Se você é um inquilino, verifique se há espaço para negociar uma redução no valor do aluguel com o proprietário. Explique sua situação e apresente argumentos válidos para uma possível negociação."
                           ]
        
        lista_lazer = ["Lazer",
                       "Procure por opções de lazer gratuitas na sua cidade, como parques, trilhas para caminhada, praias, eventos culturais gratuitos, museus com entrada gratuita em determinados dias, entre outros.",
                       "Reúna amigos e familiares para uma noite de jogos em casa. Jogos de tabuleiro, cartas, videojogos ou até mesmo uma sessão de filmes podem ser divertidos e econômicos.",
                       "Procure por cupons de desconto ou ofertas especiais em sites, aplicativos ou jornais locais. Essas promoções podem ajudar a economizar em atividades de lazer, como cinema, teatro, shows ou restaurantes.",
                       "Explore a sua biblioteca local ou centros culturais, onde você pode emprestar livros, participar de clubes de leitura, assistir a palestras ou workshops gratuitos."
                       ]
                       
        lista_transportes = ["Transportes",
                             "Opte por utilizar autocarros, metro, comboio ou outros meios de transporte público disponíveis na sua região.",
                             "Se possível, utilize a bicicleta ou faça caminhadas para trajetos curtos. Além de serem econômicos, esses meios de transporte também são benéficos para a saúde.",
                             "Esteja atento a promoções e descontos em passagens de autocarros, metro ou comboio.",
                             "Se você utiliza frequentemente o transporte público, verifique se há opções de passes mensais ou semanais com desconto. "
                             ]
        
        lista_outros = ["Outros",
                        "Tente gastar menos."
                        ]

        if count_despesas == 0:
            messagebox.showinfo("Sugestão", "Não há sugestões pois não há despesas")  
            return
        
        sugestao_aleatoria = random.randint(1, 2)
        
        if sugestao_aleatoria == 1:
            soma_alimentacao = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, lista_alimentacao[0]))
            soma_habitacao = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, lista_habitacao[0]))
            soma_lazer = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, lista_lazer[0]))
            soma_transportes = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, lista_transportes[0]))
            soma_outros = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, lista_outros[0]))
            
            print("Total Alimentacao:", soma_alimentacao)
            print("Total Habitação:", soma_habitacao)
            print("Total Lazer:", soma_lazer)
            print("Total Transportes:", soma_transportes)
            print("Total Outros:", soma_outros)

            lista_valor_categorias = []
            if soma_alimentacao >= soma_habitacao and soma_alimentacao >= soma_lazer and soma_alimentacao >= soma_transportes and soma_alimentacao >= soma_outros:
                print (soma_alimentacao)
                lista_valor_categorias.append(f"Alimentação")
            if soma_habitacao >= soma_alimentacao and soma_habitacao >= soma_lazer and soma_habitacao >= soma_outros and soma_habitacao >= soma_transportes:
                print (soma_habitacao)
                lista_valor_categorias.append(f"Habitação")
            if soma_lazer >= soma_alimentacao and soma_lazer >= soma_habitacao and soma_lazer >= soma_outros and soma_lazer >= soma_transportes:
                print (soma_lazer)
                lista_valor_categorias.append(f"Lazer")
            if soma_transportes >= soma_alimentacao and soma_transportes >= soma_habitacao and soma_transportes >= soma_lazer and soma_transportes >= soma_outros:
                print (soma_transportes)
                lista_valor_categorias.append(f"Transportes")
            if soma_outros >= soma_alimentacao and soma_outros >= soma_habitacao and soma_outros >= soma_lazer and soma_outros >= soma_transportes:
                print (soma_outros)
                lista_valor_categorias.append(f"Outros")
            
            def sugestao_aleatoria_categorias(valor_aleatorio_sugestao, categoria_testada, lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros):
                for categoria in lista_categorias:
                    if categoria == categoria_testada:
                        if categoria == lista_alimentacao[0]:
                            return f"Sugestão: {lista_alimentacao[valor_aleatorio_sugestao]}"
                        if categoria == lista_habitacao[0]:
                            return f"Sugestão: {lista_habitacao[valor_aleatorio_sugestao]}"
                        if categoria == lista_lazer[0]:
                            return f"Sugestão: {lista_lazer[valor_aleatorio_sugestao]}"
                        if categoria == lista_transportes[0]:
                            return f"Sugestão: {lista_transportes[valor_aleatorio_sugestao]}"
                        if categoria == lista_outros[0]:
                            return f"Sugestão: {lista_outros[1]}"
            
            def valor_sugestao_categorias(categoria_testada, lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros):
                for categoria in lista_categorias:
                    if categoria == categoria_testada:
                        if categoria == lista_alimentacao[0]:
                            return soma_alimentacao
                        if categoria == lista_habitacao[0]:
                            return soma_habitacao
                        if categoria == lista_lazer[0]:
                            return soma_lazer
                        if categoria == lista_transportes[0]:
                            return soma_transportes
                        if categoria == lista_outros[0]:
                            return soma_outros

            valor_aleatorio_sugestao = random.randint(2, 4)
            if len(lista_valor_categorias) == 1:
                messagebox.showinfo("Sugestão", f"""A categoria no qual gastou mais dinheiro foi:\n\n
{lista_valor_categorias[0]}: {valor_sugestao_categorias(lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}""")
            
            elif len(lista_valor_categorias) == 2:
                messagebox.showinfo("Sugestão", f"""As categorias no qual gastou mais dinheiro foram:\n\n
{lista_valor_categorias[0]}: {valor_sugestao_categorias(lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[1]}: {valor_sugestao_categorias(lista_valor_categorias[1], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[1], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}""")
            
            elif len(lista_valor_categorias) == 3:
                messagebox.showinfo("Sugestão", f"""As categorias no qual gastou mais dinheiro foram:\n\n
{lista_valor_categorias[0]}: {valor_sugestao_categorias(lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[1]}: {valor_sugestao_categorias(lista_valor_categorias[1], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[1], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[2]}: {valor_sugestao_categorias(lista_valor_categorias[2], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[2], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}""")
            
            elif len(lista_valor_categorias) == 4:
                messagebox.showinfo("Sugestão", f"""As categorias no qual gastou mais dinheiro foram:\n\n
{lista_valor_categorias[0]}: {valor_sugestao_categorias(lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[1]}: {valor_sugestao_categorias(lista_valor_categorias[1], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[1], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[2]}: {valor_sugestao_categorias(lista_valor_categorias[2], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[2], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[3]}: {valor_sugestao_categorias(lista_valor_categorias[3], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[3], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}""") 
            
            elif len(lista_valor_categorias) == 5:
                messagebox.showinfo("Sugestão", f"""As categorias no qual gastou mais dinheiro foram:\n\n
{lista_valor_categorias[0]}: {valor_sugestao_categorias(lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[0], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[1]}: {valor_sugestao_categorias(lista_valor_categorias[1], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[1], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[2]}: {valor_sugestao_categorias(lista_valor_categorias[2], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[2], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[3]}: {valor_sugestao_categorias(lista_valor_categorias[3], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[3], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}\n\n\n
{lista_valor_categorias[4]}: {valor_sugestao_categorias(lista_valor_categorias[4], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros, soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros)}€\n
{sugestao_aleatoria_categorias(valor_aleatorio_sugestao, lista_valor_categorias[4], lista_categorias, lista_alimentacao, lista_habitacao, lista_lazer, lista_transportes, lista_outros)}""")

        elif sugestao_aleatoria == 2:
            count_alimentação = int(self.clientes_lista.calcular_count_despesas_categoria_cliente_atual(self.clientes_lista, lista_alimentacao[0]))
            count_habitacao = int(self.clientes_lista.calcular_count_despesas_categoria_cliente_atual(self.clientes_lista, lista_habitacao[0]))
            count_lazer = int(self.clientes_lista.calcular_count_despesas_categoria_cliente_atual(self.clientes_lista, lista_lazer[0]))
            count_transportes = float(self.clientes_lista.calcular_count_despesas_categoria_cliente_atual(self.clientes_lista, lista_transportes[0]))
            count_outros = float(self.clientes_lista.calcular_count_despesas_categoria_cliente_atual(self.clientes_lista, lista_outros[0]))

            lista_count_categorias = []
            if count_alimentação >= count_habitacao and count_alimentação >= count_lazer and count_alimentação >= count_outros and count_alimentação >= count_transportes:
                # print (count_alimentação) #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
                lista_count_categorias.append(f"Alimentação: {count_alimentação} despesas")
            if count_habitacao >= count_alimentação and count_habitacao >= count_lazer and count_habitacao >= count_outros and count_habitacao >= count_transportes:
                # print (count_habitacao) #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
                lista_count_categorias.append(f"Habitação: {count_habitacao} despesas")
            if count_lazer >= count_alimentação and count_lazer >= count_habitacao and count_lazer >= count_outros and count_lazer >= count_transportes:
                #print (count_lazer)    #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
                lista_count_categorias.append(f"Lazer: {count_lazer} despesas")
            if count_transportes >= count_alimentação and count_transportes >= count_habitacao and count_transportes >= count_lazer and count_transportes >= count_outros:
                #print (count_transportes)  #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
                lista_count_categorias.append(f"Transportes: {count_transportes} despesas")
            if count_outros >= count_alimentação and count_outros >= count_habitacao and count_outros >= count_lazer and count_outros >= count_transportes:
                #print (count_outros)   #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
                lista_count_categorias.append(f"Outros: {count_outros} despesas")
        
            if len(lista_count_categorias) == 1:
                messagebox.showinfo("Sugestão", f"A categoria no qual fez mais despesas foi:\n\n{lista_count_categorias[0]}\n\nTente reduzir o número de despesas nesta categoria.")
            elif len(lista_count_categorias) == 2:
                messagebox.showinfo("Sugestão", f"As categorias no qual fez mais despesas foram:\n\n{lista_count_categorias[0]}\n{lista_count_categorias[1]}\n\nTente reduzir o numero de despesas nestas categorias.")
            elif len(lista_count_categorias) == 3:
                messagebox.showinfo("Sugestão", f"As categorias no qual fez mais despesas foram:\n\n{lista_count_categorias[0]}\n{lista_count_categorias[1]}\n{lista_count_categorias[2]}\n\nTente reduzir o numero de despesas nestas categorias.")
            elif len(lista_count_categorias) == 4:
                messagebox.showinfo("Sugestão", f"As categorias no qual fez mais despesas foram:\n\n{lista_count_categorias[0]}\n{lista_count_categorias[1]}\n{lista_count_categorias[2]}\n{lista_count_categorias[3]}\n\nTente reduzir o numero de despesas nestas categorias.")
            elif len(lista_count_categorias) == 5:
                messagebox.showinfo("Sugestão", f"As categorias no qual fez mais despesas foram:\n\n{lista_count_categorias[0]}\n{lista_count_categorias[1]}\n{lista_count_categorias[2]}\n{lista_count_categorias[3]}\n{lista_count_categorias[4]}\n\nTente reduzir o numero de despesas nestas categorias.")
            
            # print("Count Alimentacao:", count_alimentação)
            # print("Count Habitação:", count_habitacao) #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL
            # print("Count Lazer:", count_lazer)
            # print("Count Outros:", count_outros)
        
    def frame_ver_despesa(self):   
        username_atual = self.username
        password_atual = self.password
        self.clientes_lista.cliente_logado(username_atual, password_atual)     #Encontrar utilizador atual
        count_despesas = int(self.clientes_lista.calcular_count_despesas_cliente_atual(self.clientes_lista))

        if count_despesas == 0:
            messagebox.showinfo("Sem Despesas", "Não há despesas para exibir.")  #Falta de vareaveis importante
            return

        sorting_order_data = "asc"  #ordenação inicial da data
        sorting_order_valor = "asc"  #ordenação incial do valor
        sorting_order_categoria = "asc"  #ordenação inicial da categoria

        categorias = [] #lista que serve para armazenar as categorias
        datas = [] #lista que serve para armazenar as datas 

        def ordenar_data():
            nonlocal sorting_order_data  #indica que a variavel nao e local, referenciada acima
            items = [] #armazena os itens que serao ordenados
            children = self.tree.get_children() #vai buscar os filhos do objeto self.tree
            for child in children: #iteração de todos os filhos
                values = self.tree.item(child, "values")
                items.append((child, values)) #sao adicionados os valores que cada filho tem a lista items
            items.sort(key=lambda item: item[1][3]) #metodo sort para acessar o indice 3 
            if sorting_order_data == "desc":    #
                items.reverse()                 #
                sorting_order_data = "asc"      # serve para inverter entre descendente e ascendente
            else:                               #
                sorting_order_data = "desc"     #
            self.tree.delete(*children)                                             #   Nesta parte são eliminados todos os filhos da arvore para serem repostos 
            for item in items:                                                      #   pelos valores presentesdentro da lista items cujo ja estão ordenados na forma pretendida
                self.tree.insert("", "end", values=item[1], iid=item[0])            #   
            switch_button_data.config(text=f"Data [{sorting_order_data.upper()}]")  

        def ordenar_valor():
            nonlocal sorting_order_valor #indica que a variavel nao e local, referenciada acima
            items = [] #armazena os itens que serao ordenados
            children = self.tree.get_children() #vai buscar os filhos do objeto self.tree
            for child in children: #iteração de todos os filhos
                values = self.tree.item(child, "values")
                items.append((child, values)) #sao adicionados os valores que cada filho tem a lista items
            items.sort(key=lambda item: float(item[1][2])) #metodo sort para acessar o indice 2
            if sorting_order_valor == "desc":   #
                items.reverse()                 #
                sorting_order_valor = "asc"     # serve para inverter entre descendente e ascendente
            else:                               #
                sorting_order_valor = "desc"    #
            self.tree.delete(*children)
            for item in items:                                                          #   Nesta parte são eliminados todos os filhos da arvore para serem repostos
                self.tree.insert("", "end", values=item[1], iid=item[0])                #   pelos valores presentesdentro da lista items cujo ja estão ordenados na forma pretendida
            switch_button_valor.config(text=f"Valor [{sorting_order_valor.upper()}]")   #

        def ordenar_categoria():
            nonlocal sorting_order_categoria #indica que a variavel nao e local, referenciada acima
            items = [] #armazena os itens que serao ordenados
            children = self.tree.get_children()#vai buscar os filhos do objeto self.tree
            for child in children: #iteração de todos os filhos
                values = self.tree.item(child, "values")
                items.append((child, values)) #sao adicionados os valores que cada filho tem a lista items
            items.sort(key=lambda item: item[1][0]) #metodo sort para acessar o indice 0 
            if sorting_order_categoria == "desc":   #
                items.reverse()                     #
                sorting_order_categoria = "asc"     # serve para inverter entre descendente e ascendente
            else:                                   #
                sorting_order_categoria = "desc"    #
            self.tree.delete(*children)
            for item in items:                                                                      #   Nesta parte são eliminados todos os filhos da arvore para serem repostos
                self.tree.insert("", "end", values=item[1], iid=item[0])                            #   pelos valores presentesdentro da lista items cujo ja estão ordenados na forma pretendida
            switch_button_categoria.config(text=f"Categoria [{sorting_order_categoria.upper()}]")   #

        self.janela = tk.Tk()       #cria janela da arvore
        self.janela.title("Tabela")

        self.tree = ttk.Treeview(self.janela)  #cria arvore
        self.tree["columns"] = ("Categoria", "Descrição", "Valor", "Data")

        self.tree.heading("Categoria", text="Categoria", command=ordenar_categoria) #
        self.tree.heading("Descrição", text="Descrição")                            # headings de cada despesa
        self.tree.heading("Valor", text="Valor", command=ordenar_valor)             #
        self.tree.heading("Data", text="Data", command=ordenar_data)                #

        self.tree.column("#0", width=0)

        for i in range(0, count_despesas):
            categoria_vd = self.clientes_lista.encontrar_categoria_despesas_cliente_atual(self.clientes_lista, i) #
            descricao_vd = self.clientes_lista.encontrar_descricao_despesas_cliente_atual(self.clientes_lista, i) # valores de cada despesa
            valor_vd = self.clientes_lista.encontrar_valor_despesas_cliente_atual(self.clientes_lista, i)         #
            data_vd = self.clientes_lista.encontrar_data_despesas_cliente_atual(self.clientes_lista, i)           #
            self.tree.insert("", "end", values=(categoria_vd, descricao_vd, valor_vd, data_vd)) #insere os valores de cada despesa na tabeça     
            if categoria_vd not in categorias:
                categorias.append(categoria_vd) #serve para adicionar as categorias todas em uma lista
            if data_vd not in datas:
                datas.append(data_vd) #serve para adicionar as datas todas em uma lista

        def filtrar_por_categoria(categoria):
            self.tree.delete(*self.tree.get_children())
            if categoria == "Todas": # mostrar todas as categorias
                for i in range(0, count_despesas): #loop que vai de 0 ate ao numero de despesas
                    categoria_vd = self.clientes_lista.encontrar_categoria_despesas_cliente_atual(self.clientes_lista, i) #
                    descricao_vd = self.clientes_lista.encontrar_descricao_despesas_cliente_atual(self.clientes_lista, i) # pegar os valores de cada despesa iterada
                    valor_vd = self.clientes_lista.encontrar_valor_despesas_cliente_atual(self.clientes_lista, i)         # 
                    data_vd = self.clientes_lista.encontrar_data_despesas_cliente_atual(self.clientes_lista, i)           #
                    self.tree.insert("", "end", values=(categoria_vd, descricao_vd, valor_vd, data_vd)) #insere os valores na tree ao selecionar todas                  
            else:
                for i in range(0, count_despesas):
                    categoria_vd = self.clientes_lista.encontrar_categoria_despesas_cliente_atual(self.clientes_lista, i) # mostrar mostrar apenas a categoria para filtrar
                    if categoria_vd == categoria: #categoria escolhida
                        descricao_vd = self.clientes_lista.encontrar_descricao_despesas_cliente_atual(self.clientes_lista, i) # 
                        valor_vd = self.clientes_lista.encontrar_valor_despesas_cliente_atual(self.clientes_lista, i)         # pega todos os valores pertencentes a essa categoria em especifico
                        data_vd = self.clientes_lista.encontrar_data_despesas_cliente_atual(self.clientes_lista, i)           #
                        self.tree.insert("", "end", values=(categoria_vd, descricao_vd, valor_vd, data_vd)) #insere os valors na tree da categoria selecionada                     

        def filtrar_por_data(data):
            self.tree.delete(*self.tree.get_children())
            if data == "Todas": # mostrar todas as categorias
                for i in range(0, count_despesas): #loop que vai de 0 ate ao numero de despesas
                    categoria_vd = self.clientes_lista.encontrar_categoria_despesas_cliente_atual(self.clientes_lista, i) #
                    descricao_vd = self.clientes_lista.encontrar_descricao_despesas_cliente_atual(self.clientes_lista, i) # pegar os valores de cada despesa iterada
                    valor_vd = self.clientes_lista.encontrar_valor_despesas_cliente_atual(self.clientes_lista, i)         # 
                    data_vd = self.clientes_lista.encontrar_data_despesas_cliente_atual(self.clientes_lista, i)           #
                    self.tree.insert("", "end", values=(categoria_vd, descricao_vd, valor_vd, data_vd)) #insere os valores na tree ao selecionar todas  
            else:
                for i in range(0, count_despesas):
                    data_vd = self.clientes_lista.encontrar_data_despesas_cliente_atual(self.clientes_lista, i) # mostrar mostrar apenas a data para filtrar
                    if data_vd == data:#data escolhida
                        categoria_vd = self.clientes_lista.encontrar_categoria_despesas_cliente_atual(self.clientes_lista, i) #
                        descricao_vd = self.clientes_lista.encontrar_descricao_despesas_cliente_atual(self.clientes_lista, i) #pega todos os valores pertencentes a essa data em especifico
                        valor_vd = self.clientes_lista.encontrar_valor_despesas_cliente_atual(self.clientes_lista, i)         #
                        self.tree.insert("", "end", values=(categoria_vd, descricao_vd, valor_vd, data_vd)) #insere os valors na tree da data selecionada

        switch_button_data = ttk.Button(self.janela, text="Gráfico", command=self.grafico_pizza) #botao que ordena data
        switch_button_data.grid(row=0, column=0)

        switch_button_categoria = ttk.Button(self.janela, text="Categoria [ASC]", command=ordenar_categoria) #botao que ordena categoria
        switch_button_categoria.grid(row=0, column=1)

        switch_button_valor = ttk.Button(self.janela, text="Valor [ASC]", command=ordenar_valor) #botao que ordena valor
        switch_button_valor.grid(row=0, column=2)

        switch_button_data = ttk.Button(self.janela, text="Data [ASC]", command=ordenar_data) #botao que ordena data
        switch_button_data.grid(row=0, column=3)

        categorias.insert(0, "Todas")                                                                               #
        combo_categoria = ttk.Combobox(self.janela, values=categorias, state="readonly")                            #
        combo_categoria.bind("<<ComboboxSelected>>", lambda event: filtrar_por_categoria(combo_categoria.get()))    # Combobox para filtrar categorias 
        combo_categoria.current(0)                                                                                  #
        combo_categoria.grid(row=0, column=4)                                                                       #

        datas.insert(0, "Todas")                                                                                    #
        combo_data = ttk.Combobox(self.janela, values=datas, state="readonly")                                      #
        combo_data.bind("<<ComboboxSelected>>", lambda event: filtrar_por_data(combo_data.get()))                   # Combobox para filtrar datas
        combo_data.current(0)                                                                                       #
        combo_data.grid(row=0, column=5)                                                                            #

        self.tree.grid(row=1, column=0, columnspan=6)

        self.janela.mainloop()

    def grafico_pizza(self):
        username_atual = self.username
        password_atual = self.password
        self.clientes_lista.cliente_logado(username_atual, password_atual)     #Encontrar utilizador atual
        
        soma_alimentacao = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, "Alimentação"))
        soma_habitacao = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, "Habitação"))
        soma_lazer = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, "Lazer"))
        soma_transportes = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, "Transportes"))
        soma_outros = float(self.clientes_lista.calcular_total_despesas_categoria_atual(self.clientes_lista, "Outros"))

        valores = [soma_alimentacao, soma_habitacao, soma_lazer, soma_transportes, soma_outros]
        labels = ["Alimentação", "Habitação", "Lazer", "Transportes", "Outros"]

        # Filtrar as categorias com valores zero
        valores_filtrados = []
        labels_filtrados = []
        for valor, label in zip(valores, labels):
            if valor != 0:
                valores_filtrados.append(valor)
                labels_filtrados.append(label)

        # Criar o gráfico de pizza apenas com as categorias com valores diferentes de zero
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(valores_filtrados, labels=labels_filtrados, autopct='%1.1f%%', startangle=90)
        ax.set_title('Gastos por Categoria')

        # Exibir os valores das categorias abaixo do gráfico
        total = sum(valores_filtrados)
        percent_format = '%1.1f%%'
        for i, (label, autotext) in enumerate(zip(labels_filtrados, autotexts)):
            percent = valores_filtrados[i] / total * 100
            value_label = f'{valores_filtrados[i]:.2f}€'
            autotext.set_text(f'{value_label}\n({percent_format % percent})')

        # Ajustar o layout para evitar sobreposição das anotações
        plt.tight_layout()

        # Exibir o gráfico
        plt.show()

    def frame_definir_orcamento(self): #frame ver orçamento
        if self.frame:
            self.frame.destroy()    #eliminar a frame

        self.master.geometry("500x200")
        self.master.title("Orçamento")
        self.master.resizable(False, False)     #delimitadores de frame 
        self.frame = tk.Frame(self.master, bg='#0076a3')
        self.frame.pack(fill=tk.BOTH , expand=True)
        self.invisivel = tk.Label(self.frame, text="                                              ", bg="#0076a3")#Para ficar direito com o resto
        self.invisivel.grid(row=0,column=0)
        
        self.gastos_label = tk.Label(self.frame, text="Máximo de gastos para o mês",font=("Arial"), fg="#ffffff", bg="#0076a3") #gastos label
        self.gastos_label.grid(row=1, column=1)
        self.gastos_entry = tk.Entry(self.frame) #entry gastos
        self.gastos_entry.grid(row=2, column=1, pady=5)
        valor_numerico_gastos = self.master.register(self.verificar_numerico) #verificacao para apenas escrever numerico e .
        self.gastos_entry.config(validate="key", validatecommand=(valor_numerico_gastos, "%P"))    

        self.orcamento_label = tk.Label(self.frame, text="Orçamento",font=("Arial"), fg="#ffffff", bg="#0076a3") #orcamento label
        self.orcamento_label.grid(row=3, column=1)
        self.orcamento_entry = tk.Entry(self.frame) #orcamento valor
        self.orcamento_entry.grid(row=4, column=1, pady=5)
        valor_numerico_orcamento = self.master.register(self.verificar_numerico) #verificacao para apenas escrever numerico e .
        self.orcamento_entry.config(validate="key", validatecommand=(valor_numerico_orcamento, "%P"))  
        
        self.definir_orc_button = tk.Button(self.frame, text="DEFINIR",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.definir_orcamento) #botao para definir orçamento
        self.definir_orc_button.grid(row=5, column=1)

        self.voltar_button = tk.Button(self.frame, text="VOLTAR",font=("Arial",10), fg="#000000", bg="#ffffff", command=self.frame_menu) #botao voltar
        self.voltar_button.grid(row=6, column=1)

    def definir_orcamento(self):
        gastos_mes = self.gastos_entry.get()
        orcamento = self.orcamento_entry.get()

        verificacao_orcamento = True
        if len(gastos_mes) == 0:  #missing input error
            messagebox.showinfo("Erro", "Defina os gastos para o mês")
            verificacao_orcamento = False
        if len(orcamento) == 0:   #missing input error
            messagebox.showinfo("Erro", "Defina o orçamento")
            verificacao_orcamento = False
        
        if verificacao_orcamento == False:
            if self.frame:
                self.frame.destroy()    #destruir a frame
                self.frame_definir_orcamento() 
    
        if verificacao_orcamento == True:                 # verificacao logica de variaveis 
            self.gastos_mes_final_verificacao = float(gastos_mes)
            self.orcamento_final_verificacao = float(orcamento)
            if self.gastos_mes_final_verificacao > self.orcamento_final_verificacao:
                messagebox.showinfo("Erro", "Gastos para o mês superiores ao orçamento")
                verificacao_orcamento = False
        
        if verificacao_orcamento == False:
            if self.frame:
                self.frame.destroy()    #destruir a frame
                self.frame_definir_orcamento() 

        if verificacao_orcamento == True:                      #passou a verificacao inicial de erros 
            verificacao_orcamento_2 = True
            self.gastos_mes_final_verificacao = float(gastos_mes)
            self.orcamento_final_verificacao = float(orcamento)

            orcamento_final = Orcamento(self.gastos_mes_final_verificacao, self.orcamento_final_verificacao) #adicionar as despesas na classe Despesa
            self.despesas_lista.append_orcamento(orcamento_final) #adicionar as despesas na linked list
            
            username_atual = self.username
            password_atual = self.password
            self.clientes_lista.cliente_logado(username_atual, password_atual)
            confirmacao_orcamento = messagebox.askyesno("Confirmação", f"Deseja submeter o orcamento de:\n\nOrcamento: {self.orcamento_final_verificacao}€\nGastos Mensais: {self.gastos_mes_final_verificacao}€")
            if confirmacao_orcamento == True:    
                if self.clientes_lista.adicionar_orcamento_cliente_logado(gastos_mes, orcamento) == 1: #erro ja tem orcamento
                    messagebox.showinfo("Erro", "O cliente já possui um orçamento.")
                    verificacao_orcamento_2 = False    
                else:
                    #self.clientes_lista.print_list_cliente_despesas_orcamento()  #CASO QUEIRA VERIFICAR OS VALORES NO TERMINAL  
                    messagebox.showinfo("Sucesso", "Orçamento criado com sucesso.")

                if verificacao_orcamento_2 == False:
                    if self.frame:
                        self.frame.destroy()    #destruir a frame
                        self.frame_menu() 
                
                if self.frame:
                    self.frame.destroy()    #destruir a frame
                    self.frame_menu()  
            else:
                if self.frame:
                    self.frame.destroy()    #destruir a frame
                    self.frame_definir_orcamento()
        
    def tamanho_password(self, tamanho):    #função que serve para verificar o tamaho da password
        if len(tamanho) <= 16 :
            return True
        else:
            self.master.bell() 
            return False
        
    def verificar_numerico(self, valor): #função para apenas escrever numerico ou .
        return re.match(r"^\d*\.?\d*$", valor) is not None #biblioteca para verificar se o valor escrito é numerico ou um .
    
    def save_lists_to_json(self):
        filename = "dados.json"
        data = {
            "clientes": self.clientes_lista.to_json(),
            "despesas": self.despesas_lista.to_json(),
            "orcamento": self.orcamento_lista.to_json()
        }

        with open(filename, 'w') as json_file:
            json.dump(data, json_file)

        if self.frame:
            exit()

    def load_lists_from_json(self):
        # Verificar se existem os arquivos JSON correspondentes às listas
        if os.path.exists("clientes.json") and os.path.exists("despesas.json") and os.path.exists("orcamento.json"):
            # Carregar os dados dos arquivos JSON
            with open("clientes.json", "r") as file:
                clientes_json = json.load(file)
            with open("despesas.json", "r") as file:
                despesas_json = json.load(file)
            with open("orcamento.json", "r") as file:
                orcamento_json = json.load(file)

            # Transformar os dados JSON em listas
            self.from_json(clientes_json)
            self.despesas_lista.from_json(despesas_json)
            self.orcamento_lista.from_json(orcamento_json)