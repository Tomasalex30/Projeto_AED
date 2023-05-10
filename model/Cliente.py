from model.Lista.LinkedList import *

class Cliente:
    def init(self, nome, password, nif):
        self.nome = nome
        self.password = password
        self.nif = nif

    def get_nome(self):
        return self.nome
    def set_nome(self, novo_nome):
        self.nome = novo_nome

    def get_password(self):
        return self.password
    def set_password(self, nova_password):
        self.password = nova_password

    def get_nif(self):
        return self.nif
    def set_nif(self, novo_nif):
        self.nif = novo_nif