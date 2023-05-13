from model.Lista.LinkedListCliente import *

class Orcamento:
    def __init__(self, gastos_mes, orcamento, count_orcamento):
        self.gastos_mes = gastos_mes
        self.orcamento = orcamento
        self.count_orcamento = count_orcamento
        
    def get_gastos_mes(self): #pega valor
        return self.gastos_mes
    def set_gastos_mes(self, novo_gastos_mes): #mete valor
        self.valor = novo_gastos_mes

    def get_orcamento(self): #pega valor
        return self.orcamento
    def set_orcamento(self, novo_orcamento): #mete valor
        self.valor = novo_orcamento

    def get_count_orcamento(self): #pega valor
        return self.count_orcamento
    def set_count_orcamento(self, novo_count_orcamento): #mete valor
        self.count_orcamento = novo_count_orcamento