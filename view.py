import tkinter as tk
from tkinter import messagebox
from model.Cliente import *
from model.Lista.LinkedList import *
from model.Lista.Iterador import *

class View:

    def __init__(self, master):
        self.clientes_lista = LinkedList()
        self.master = master
        self.master.geometry("500x300")
        self.master.title("Inicio")
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.frame_inicial()
    
    def frame_inicial(self):   #frame login 
        if self.frame:
            self.frame.destroy()
        
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="USERNAME")
        self.label.grid(row=0, column=0)    #.pack()
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=1, column=0, pady=5)   #.pack()

        self.password_label = tk.Label(self.frame, text="PASSWORD")
        self.password_label.grid(row=2, column=0)   #.pack()
        validar_password = (self.master.register(self.tamanho_password), '%P')
        self.password_entry = tk.Entry(self.frame, show='*', validate='key', validatecommand=validar_password, width=16)
        self.password_entry.grid(row=3, column=0)

        self.voltar_button = tk.Button(self.frame, text="VER/OCULTAR", command=self.ver_login)
        self.voltar_button.grid(row=3, column=1)

        self.login_button = tk.Button(self.frame, text="LOGIN", command=self.login)
        self.login_button.grid(row=4, column=0) #.pack()
        
        self.register_button = tk.Button(self.frame, text="REGISTER", command=self.frame_registo) #ver nova frame
        self.register_button.grid(row=5, column=0)  #.pack()

        self.quit_button = tk.Button(self.frame, text="SAIR", command=exit)
        self.quit_button.grid(row=6, column=0)  #.pack()

    def frame_registo(self): #frame registo
        if self.frame:
            self.frame.destroy()
        
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.master.geometry("500x300")
        self.master.title("Registo")
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.nome_label = tk.Label(self.frame, text="NOME")
        self.nome_label.grid(row=0, column=0)   #.pack()
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=1, column=0, pady=5)   #.pack()

        self.password_label = tk.Label(self.frame, text="PASSWORD")
        self.password_label.grid(row=2, column=0)   #.pack()
        validar_password = (self.master.register(self.tamanho_password), '%P')
        self.password_entry = tk.Entry(self.frame, show='*', validate='key', validatecommand=validar_password, width=16)
        self.password_entry.grid(row=3, column=0)
        self.password_label_2 = tk.Label(self.frame, text="REPETIR PASSWORD")
        self.password_label_2.grid(row=4, column=0)   #.pack()
        validar_password = (self.master.register(self.tamanho_password), '%P')
        self.password_entry_2 = tk.Entry(self.frame, show='*', validate='key', validatecommand=validar_password, width=16)
        self.password_entry_2.grid(row=5, column=0)
        self.info_password = tk.Label(self.frame, text="A palavra passe deve ter no máximo 16 carácteres")
        self.info_password.grid(row=10, column=0)


        self.ver_ocultar_button = tk.Button(self.frame, text="VER/OCULTAR", command=self.ver_registo)
        self.ver_ocultar_button.grid(row=3, column=1)
         
        self.nif_label = tk.Label(self.frame, text="NIF")
        self.nif_label.grid(row=6, column=0)
        validar = (self.master.register(self.tamanho_nif), '%P')
        self.nif_entry = tk.Entry(self.frame, validate='key', validatecommand=validar, width=9)
        self.nif_entry.grid(row=7, column=0, pady=5)
        
        self.login_button = tk.Button(self.frame, text="REGISTAR", command=self.registar)
        self.login_button.grid(row=8, column=0) #.pack()
        
        self.voltar_button = tk.Button(self.frame, text="VOLTAR", command=self.frame_inicial)
        self.voltar_button.grid(row=9, column=0)    #.pack()

        
    def registar(self):
        nome_registo = self.nome_entry.get()
        password_registo = self.password_entry.get()
        password_registo_2 = self.password_entry_2.get()
        nif = self.nif_entry.get()
        
        verificacao_registo = True
        if len(nome_registo)==0 :
            messagebox.showinfo("Erro", "Complete o nome")
            verificacao_registo = False

        if len(password_registo)==0  :
            messagebox.showinfo("Erro", "Complete a password")
            verificacao_registo = False

        if len(password_registo_2)==0  :
            messagebox.showinfo("Erro", "Complete a confirmação de password")
            verificacao_registo = False

        if password_registo != password_registo_2 and len(password_registo_2)>0 and len(password_registo)>0:
            messagebox.showinfo("Erro", "Passwords diferentes")
            verificacao_registo = False

        if len(nif)==0:
            messagebox.showinfo("Erro", "Complete o NIF") 
            verificacao_registo = False

        if len(password_registo) > 0 and len(password_registo) < 8:
            messagebox.showinfo("Erro", "Password Pequena") 
            verificacao_registo = False

        if len(nif) > 0 and len(nif) < 9:
            messagebox.showinfo("Erro", "NIF Pequeno")
            verificacao_registo = False

        for cliente in self.clientes_lista:
            if cliente.get_nome() == nome_registo:
                messagebox.showinfo("Erro", "Nome de registo já existente")
                verificacao_registo = False
                break

        for cliente in self.clientes_lista:
            if cliente.get_nif() == nif:
                messagebox.showinfo("Erro", "NIF já existente")
                verificacao_registo = False
                break

        if verificacao_registo == False:
            if self.frame:
                self.frame.destroy()
                self.frame_registo()

        if verificacao_registo == True:
            cliente = Cliente()
            cliente.set_nome(nome_registo)
            cliente.set_password(password_registo)
            cliente.set_nif(nif)
            self.clientes_lista.append(cliente)
            self.clientes_lista.print_list()
                
            if self.frame:
                self.frame.destroy()
                self.frame_inicial()
            
    def login(self):
        username_login = self.nome_entry.get()
        password_login = self.password_entry.get()
        
        verificacao_login = True
        if len(username_login)==0 :
            messagebox.showinfo("Erro", "Complete o nome")
            verificacao_login = False

        if len(password_login)==0 :
            messagebox.showinfo("Erro", "Complete a password")
            verificacao_login = False

        if len(password_login) > 0 and len(password_login) < 8:
            messagebox.showinfo("Erro", "Password Pequena") 
            verificacao_login = False
        
        if verificacao_login == False:
            if self.frame:
                self.frame.destroy()
                self.frame_inicial()

        if verificacao_login == True:
            count = 0
            for cliente in self.clientes_lista:
                if cliente != None:
                    count += 1
            if count == 0:
                messagebox.showinfo("Erro", "Não existem Utilizadores Registados") 
                verificacao_login = False
            
            if verificacao_login == True:
                cliente_encontrado = None
                for cliente in self.clientes_lista:
                    if cliente.get_nome() == username_login and cliente.get_password() == password_login:
                        cliente_encontrado = cliente
                        break
                
                if cliente_encontrado:
                    messagebox.showinfo("Sucesso", "Login bem-sucedido")
                    #continuar aqui login 
                else:
                    messagebox.showinfo("Erro", "Credenciais inválidas")
                    if self.frame:
                        self.frame.destroy()
                        self.frame_inicial()

    def ver_registo(self):
        if self.password_entry["show"] == "*" and self.password_entry_2["show"] == "*" :
            self.password_entry["show"] = ""
            self.password_entry_2["show"] = ""
        else :
            self.password_entry["show"] ="*"
            self.password_entry_2["show"] = "*"
    
    def ver_login(self):
        if self.password_entry["show"] == "*":
            self.password_entry["show"] = ""
        else:
            self.password_entry["show"] ="*"

    def tamanho_password(self, tamanho):
        if len(tamanho) <= 16 :
            return True
        else:
            self.master.bell() 
            return False
    
    def tamanho_nif(self, tamanho):
        if len(tamanho) <= 9:
            return True
        else:
            self.master.bell()  
            return False