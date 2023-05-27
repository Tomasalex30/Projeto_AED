from model.Lista.LinkedListCliente import *
from model.Lista.LinkedListDespesas import *

class Cliente:
    def __init__(self, nome, password, nif):
        self.nome = nome
        self.password = password
        self.nif = nif
        self.lista = None
        self.despesas = LinkedListDespesas() #serve para poder armazenar a linkedlist de despesas na classe cliente
        self.orcamento = LinkedListDespesas()
        self.orcamento_count = 0

    def get_nome(self): #pega nome
        return self.nome
    def set_nome(self, novo_nome): #mete nome
        self.nome = novo_nome

    def get_password(self): #pega password
        return self.password
    def set_password(self, nova_password):  #mete password
        self.password = nova_password

    def get_nif(self):  #pega nif
        return self.nif
    def set_nif(self, novo_nif): #mete nif
        self.nif = novo_nif

    def get_lista(self): #pega lista
        return self.lista
    def set_lista(self, nova_lista): #mete lista
        self.lista = nova_lista

    def to_dict(self):
        return {
            "nome": self.nome,
            "password": self.password,
            "nif": self.nif
        }
