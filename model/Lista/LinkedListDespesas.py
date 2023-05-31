from model.Lista.Nodes import *
from model.Cliente import *
from model.Despesas import *
from model.Orcamento import *
from view import *

class LinkedListDespesas:
    def __init__(self): #construtores
        self.head = None
        self.tail = None

    def append_despesas(self, value): #adicionar despesas
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
    
    def append_orcamento(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node
            new_node.prev = current_node

    def remove_despesas(self, value): #remover despesas
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

    def __iter__(self): #iterar despesas
        current_node = self.head
        while current_node is not None:
            yield current_node.value
            current_node = current_node.next

    def print_list_despesas(self): #printar despesas
        current_node = self.head
        while current_node is not None:
            print("Categoria:", current_node.value.get_categoria())
            print("Descrição", current_node.value.get_descricao())
            print("Valor", current_node.value.get_valor())
            print("Data", current_node.value.get_data())
            print()
            current_node = current_node.next

    def to_json(self):     #Passar dde linked list para dicionario
        json_data = []
        current = self.head
        while current:
            json_data.append(current.value.to_dict())
            current = current.next
        return json_data
    
    def from_json(self, json_data):           #Passar de dicionario para linked list
        self.head = None
        self.tail = None
        for item in json_data:
            despesas_dict = item  # Assuming each item in json_data is a dictionary representing a node value (despesas)
            despesas = Despesas(despesas_dict["categoria"], despesas_dict["descricao"], despesas_dict["valor"], despesas_dict["data"])
            self.append_despesas(despesas)