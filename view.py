import tkinter as tk
import re
import matplotlib.pyplot as plt
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
        
        self.register_button = tk.Button(self.frame, text="REGISTAR", command=self.frame_registo) #ver nova frame
        self.register_button.grid(row=5, column=0)  #Botao Registar - pag inicial

        self.quit_button = tk.Button(self.frame, text="SAIR", command=exit)
        self.quit_button.grid(row=6, column=0)  #Botao Sair do programa - pag inicial

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
        
        self.adicionar_depesas = tk.Button( self.frame ,text = "Adicionar despesas: ", command=self.frame_adicionar_despesas) #botao adicionar despesas
        self.adicionar_depesas.grid(row=3 , column=1,)
        
        self.ver_depesas = tk.Button( self.frame , text = "Ver despesas: ", command = self.frame_ver_despesa) #botao ver despesas
        self.ver_depesas.grid(row=5 , column=1,)
        
        self.orcamento = tk.Button(self.frame ,  text= "Definir orçamento mensal:", command= self.frame_definir_orcamento) #botao definir orçamento
        self.orcamento.grid(row=7 , column=1)

        self.sign_out = tk.Button(self.frame ,  text= "SIGN OUT", command= self.frame_login) #botao voltar
        self.sign_out.grid(row=9 , column=1)

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
            values=["Selecione a Categoria", "Alimentação", "Lazer", "Habitação", "Outros"]  #valores da categoria a escolher
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

        gastos_mes_cliente_atual = float(self.clientes_lista.encontrar_gastos_mes_cliente_atual(self.clientes_lista)) #função que recolhe os gastos do mes definidos pelo cliente
        orcamento_cliente_atual = float(self.clientes_lista.encontrar_orcamento_cliente_atual(self.clientes_lista))  #função que recolhe o orcamento do mes definidos pelo cliente
        total_despesas_cliente_atual = float(self.clientes_lista.calcular_total_despesas_cliente_atual(self.clientes_lista)) #função que soma todas as despesas do cliente
        resto_gastos_mes = gastos_mes_cliente_atual - total_despesas_cliente_atual #gastos do mes atual
        resto_orcamento = orcamento_cliente_atual - total_despesas_cliente_atual #orcamento atual
        
        if gastos_mes_cliente_atual != 0 or orcamento_cliente_atual != 0: #serve para verificar se existe orcamento ou gastos do mes para o texto
            self.nome_label = tk.Label(self.frame, text=f"Resta-lhe {resto_gastos_mes}€ de limite de gastos do mês")
            self.nome_label.grid(row=5, column=0)
            self.nome_label = tk.Label(self.frame, text=f"Resta-lhe {resto_orcamento}€ de orçamento")
            self.nome_label.grid(row=6, column=0)
        else:
            self.nome_label = tk.Label(self.frame, text=f"Não tem limite de gastos do mês")
            self.nome_label.grid(row=5, column=0)
            self.nome_label = tk.Label(self.frame, text=f"Não têm orçamento")
            self.nome_label.grid(row=6, column=0)
    
    def adicionar_despesas(self): #função adicionar despesas
        categoria = self.combo.get() #valor entry categoria
        descricao = self.descricao_entry.get() #valor entry descrição
        valor = self.valor_entry.get() #valor entry valor
        data = self.data_entry.get() #valor entry data

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
                self.frame.destroy()
                self.frame_adicionar_despesas()

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
                                self.clientes_lista.print_list_cliente_despesas_orcamento()
                                total_despesas_cliente_atual = float(self.clientes_lista.calcular_total_despesas_cliente_atual(self.clientes_lista))
                                resto_gastos_mes = gastos_mes_cliente_atual - total_despesas_cliente_atual #gastos do mes atual
                                resto_orcamento = orcamento_cliente_atual - total_despesas_cliente_atual #orcamento atual
                                print()
                                print("Total Despesas", total_despesas_cliente_atual)
                                print("Resto dos gastos do mes",resto_gastos_mes)
                                print("Resto orcamento", resto_orcamento)
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
                    messagebox.showinfo("Erro", "Excedeu os gastos do mês")       #Erro excedeu os gastos do mes
                    verificacao_despesas_2 = 1    
            else:
                messagebox.showinfo("Erro", "O cliente precisa criar um orçamento antes de adicionar despesas.")     #Erro falta de variavel importante
                verificacao_despesas_2 = 1
            
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

        switch_button_categoria = ttk.Button(self.janela, text="Categoria [ASC]", command=ordenar_categoria) #botao que ordena categoria
        switch_button_categoria.grid(row=0, column=0)

        switch_button_valor = ttk.Button(self.janela, text="Valor [ASC]", command=ordenar_valor) #botao que ordena valor
        switch_button_valor.grid(row=0, column=1)

        switch_button_data = ttk.Button(self.janela, text="Data [ASC]", command=ordenar_data) #botao que ordena data
        switch_button_data.grid(row=0, column=2)

        categorias.insert(0, "Todas")                                                                               #
        combo_categoria = ttk.Combobox(self.janela, values=categorias, state="readonly")                            #
        combo_categoria.bind("<<ComboboxSelected>>", lambda event: filtrar_por_categoria(combo_categoria.get()))    # Combobox para filtrar categorias 
        combo_categoria.current(0)                                                                                  #
        combo_categoria.grid(row=0, column=3)                                                                       #

        datas.insert(0, "Todas")                                                                                    #
        combo_data = ttk.Combobox(self.janela, values=datas, state="readonly")                                      #
        combo_data.bind("<<ComboboxSelected>>", lambda event: filtrar_por_data(combo_data.get()))                   # Combobox para filtrar datas
        combo_data.current(0)                                                                                       #
        combo_data.grid(row=0, column=4)                                                                            #

        self.tree.grid(row=1, column=0, columnspan=5)

        self.janela.mainloop()
        
    def frame_definir_orcamento(self): #frame ver orçamento
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
                    self.clientes_lista.print_list_cliente_despesas_orcamento()   #criar orcamento
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
                
    def eliminar_conta(self):
        linked_list_cliente = LinkedListCliente()
        current_client = linked_list_cliente.cliente_logado()
        linked_list_cliente.remove_cliente(linked_list_cliente.cliente_atual)
        if self.frame:
            self.frame.destroy()              #Destruicao da frame
            self.frame_login()
        
    def tamanho_password(self, tamanho):    #função que serve para verificar o tamaho da password
        if len(tamanho) <= 16 :
            return True
        else:
            self.master.bell() 
            return False
        
    def verificar_numerico(self, valor): #função para apenas escrever numerico ou .
        return re.match(r"^\d*\.?\d*$", valor) is not None #biblioteca para verificar se o valor escrito é numerico ou um .


    
    