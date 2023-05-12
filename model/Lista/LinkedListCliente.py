from model.Lista.Nodes import *
from model.Cliente import *
from model.Despesas import *
from view import *
import os

class LinkedListCliente:
    def __init__(self): #construtor
        self.head = None
        self.tail = None
        self.cliente_atual = None

    def append_cliente(self, value): #adicionar cliente
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node
            new_node.prev = current_node
            self.tail = new_node

    def remove_cliente(self, value): #remover cliente
        if self.head is None:
            return
        current_node = self.head
        while current_node is not None:
            if current_node.value == value:
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                else:
                    self.head = current_node.next
                if current_node.next is not None:
                    current_node.next.prev = current_node.prev
                else:
                    self.tail = current_node.prev
                break
            current_node = current_node.next

    def __iter__(self): #iterar 
        current_node = self.head
        while current_node is not None:
            yield current_node.value
            current_node = current_node.next

    def cliente_logado(self, username, password):
        current_node = self.head
        while current_node is not None:
            if current_node.value.get_nome() == username and current_node.value.get_password() == password:
                self.cliente_atual = current_node.value
                print(username)
                print(password)
                break
            current_node = current_node.next
        else:
            print("Nome de usuário ou senha incorretos.")
    
    def adicionar_despesa_cliente_logado(self, categoria, descricao, valor, data):
        if self.cliente_atual is None:
            print("Nenhum cliente está logado.")
            return
        nova_despesa = Despesas(categoria, descricao, valor, data)
        self.cliente_atual.despesas.append_despesas(nova_despesa)
        print("Despesa adicionada ao cliente:", self.cliente_atual.get_nome())
    
    def print_list_cliente_despesas(self):
        current_node = self.head
        os.system("cls")
        print("Utilizadores Registados:")
        print()
        while current_node is not None:
            cliente = current_node.value
            print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print()
            print("Nome:", cliente.get_nome())
            print("Password:", cliente.get_password())
            print("NIF:", cliente.get_nif())
            print("Despesas:")
            print()
            for despesa in cliente.despesas:
                print("  Categoria:", despesa.get_categoria())
                print("  Descrição:", despesa.get_descricao())
                print("  Valor:", despesa.get_valor())
                print("  Data:", despesa.get_data())
                print()
            current_node = current_node.next
    
    def print_list_cliente(self): #printar ciente
        current_node = self.head
        os.system("cls")
        print("Utilizadores Registados:")
        print()
        while current_node is not None:
            cliente = current_node.value
            print("Nome:", current_node.value.get_nome())
            print("Password:", current_node.value.get_password())
            print("NIF:", current_node.value.get_nif())
            print()
            current_node = current_node.next