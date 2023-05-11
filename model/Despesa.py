from model.Lista.LinkedList import *

class Despesa:
    def __init__(self, categoria, descricao, valor, data):
        self.categoria = categoria
        self.descricao =descricao 
        self.valor = valor
        self.data = data
        
    def get_nome(self):
        return self.categoria
    def set_nome(self, nova_categoria):
        self.categoria = nova_categoria

    def get_descricao(self):
        return self.descricao
    def set_descricao(self, nova_descricao):
        self.descricao = nova_descricao

    def get_valor(self):
        return self.valor
    def set_valor(self, novo_valor):
        self.valor = novo_valor

    def get_data(self):
        return self.descricao
    def set_data(self, nova_data):
        self.data = nova_data