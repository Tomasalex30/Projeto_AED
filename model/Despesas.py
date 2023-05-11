from model.Lista.LinkedListCliente import *

class Despesas:
    def __init__(self, categoria, descricao, valor, data):
        self.categoria = categoria
        self.descricao =descricao 
        self.valor = valor
        self.data = data
        
    def get_categoria(self): #pega categoria
        return self.categoria
    def set_categoria(self, nova_categoria): #mete categoria
        self.categoria = nova_categoria

    def get_descricao(self): #pega descrição
        return self.descricao
    def set_descricao(self, nova_descricao): #mete descrição
        self.descricao = nova_descricao

    def get_valor(self): #pega valor
        return self.valor
    def set_valor(self, novo_valor): #mete valor
        self.valor = novo_valor

    def get_data(self): #pega data
        return self.descricao
    def set_data(self, nova_data): #mete data
        self.data = nova_data