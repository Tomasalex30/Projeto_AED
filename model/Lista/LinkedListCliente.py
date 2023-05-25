from model.Lista.Nodes import *
from model.Cliente import *
from model.Despesas import *
from model.Orcamento import *
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
                break
            current_node = current_node.next
        else:
            return False
         
    def calcular_total_despesas_cliente_atual(slef, lista_clientes):
        if lista_clientes.cliente_atual is None:
            return 0
        total_despesas = 0
        despesas_cliente_atual = lista_clientes.cliente_atual.despesas
        current_node = despesas_cliente_atual.head
        while current_node is not None:
            valor_despesa = float(current_node.value.get_valor())
            total_despesas += valor_despesa
            current_node = current_node.next
        lista_clientes.cliente_atual.total_despesas = total_despesas
        return total_despesas
    
    def calcular_total_despesas_categoria_atual(slef, lista_clientes, categoria):
        if lista_clientes.cliente_atual is None:
            return 0
        total_despesas = 0
        despesas_cliente_atual = lista_clientes.cliente_atual.despesas
        current_node = despesas_cliente_atual.head
        while current_node is not None:
            if current_node.value.get_categoria() == categoria:
                valor_despesa = float(current_node.value.get_valor())
                total_despesas += valor_despesa
            current_node = current_node.next
        return total_despesas
    
    def calcular_count_despesas_categoria_cliente_atual(self, lista_clientes, categoria):
        if lista_clientes.cliente_atual is None:
            return 0
        count_despesas = 0
        despesas_cliente_atual = lista_clientes.cliente_atual.despesas
        current_node = despesas_cliente_atual.head
        while current_node is not None:
            if current_node.value.get_categoria() == categoria:
                count_despesas += 1
            current_node = current_node.next
        lista_clientes.cliente_atual.numero_despesas_categoria = count_despesas
        return count_despesas
    
    def calcular_count_despesas_cliente_atual(self, lista_clientes):
        if lista_clientes.cliente_atual is None:
            return 0
        count_despesas = 0
        despesas_cliente_atual = lista_clientes.cliente_atual.despesas
        current_node = despesas_cliente_atual.head
        while current_node is not None:
            count_despesas += 1
            current_node = current_node.next
        lista_clientes.cliente_atual.numero_despesas = count_despesas
        return count_despesas
    
    def calcular_count_orcamento_cliente_atual(self, lista_clientes):
        if lista_clientes.cliente_atual is None:
            return 0
        count_orcamento = 0
        orcamento_cliente_atual = lista_clientes.cliente_atual.orcamento
        current_node = orcamento_cliente_atual.head
        while current_node is not None:
            count_orcamento += 1
            current_node = current_node.next
        lista_clientes.cliente_atual.numero_orcamento = count_orcamento
        return count_orcamento
                
    def encontrar_gastos_mes_cliente_atual(self, clientes_lista):
        if clientes_lista.cliente_atual is None:
            return 0
        orcamento = clientes_lista.cliente_atual.orcamento.head
        if orcamento is not None:
            return orcamento.value.get_gastos_mes()
        return 0
    
    def encontrar_categoria_despesas_cliente_atual(self, clientes_lista, posicao):
        if clientes_lista.cliente_atual is None:
            return None
        despesas_cliente_atual = clientes_lista.cliente_atual.despesas
        current_node = despesas_cliente_atual.head
        count = 0
        while current_node is not None:
            if count == posicao:
                return current_node.value.get_categoria()
            count += 1
            current_node = current_node.next
        return None

    def encontrar_descricao_despesas_cliente_atual(self, clientes_lista, posicao):
        if clientes_lista.cliente_atual is None:
            return None
        despesas_cliente_atual = clientes_lista.cliente_atual.despesas
        current_node = despesas_cliente_atual.head
        count = 0
        while current_node is not None:
            if count == posicao:
                return current_node.value.get_descricao()
            count += 1
            current_node = current_node.next
        return None

    def encontrar_valor_despesas_cliente_atual(self, clientes_lista, posicao):
        if clientes_lista.cliente_atual is None:
            return None
        despesas_cliente_atual = clientes_lista.cliente_atual.despesas
        current_node = despesas_cliente_atual.head
        count = 0
        while current_node is not None:
            if count == posicao:
                return current_node.value.get_valor()
            count += 1
            current_node = current_node.next
        return None

    def encontrar_data_despesas_cliente_atual(self, clientes_lista, posicao):
        if clientes_lista.cliente_atual is None:
            return None
        despesas_cliente_atual = clientes_lista.cliente_atual.despesas
        current_node = despesas_cliente_atual.head
        count = 0
        while current_node is not None:
            if count == posicao:
                return current_node.value.get_data()
            count += 1
            current_node = current_node.next
        return None

    def encontrar_orcamento_cliente_atual(self, clientes_lista):
        if clientes_lista.cliente_atual is None:
            return 0
        orcamento = clientes_lista.cliente_atual.orcamento.head
        if orcamento is not None:
            return orcamento.value.get_orcamento()
        return 0

    def verificar_orcamento(self):
        if self.cliente_atual is None:
            return 0
        if self.cliente_atual.orcamento_count == 0:
            return 1

    def adicionar_despesa_cliente_logado(self, categoria, descricao, valor, data):
        if self.cliente_atual is None:
            return
        nova_despesa = Despesas(categoria, descricao, valor, data)
        self.cliente_atual.despesas.append_despesas(nova_despesa)
        return 1 

    def adicionar_orcamento_cliente_logado(self, gastos_mes, orcamento):
        if self.cliente_atual is None:
            return
        if self.cliente_atual.orcamento_count > 0:
            return 1
        novo_orcamento = Orcamento(gastos_mes, orcamento)
        self.cliente_atual.orcamento.append_orcamento(novo_orcamento)
        self.cliente_atual.orcamento_count += 1
        return 2
    
    def bubble_sort(self, colecao):
        for i in range(len(colecao)):
            for j in range(len(colecao) - i - 1):
                if colecao[j] > colecao [j + 1]:
                    tmp = colecao[j + 1]
                    colecao[j + 1] = colecao[j]
                    colecao[j] = tmp
    
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
            print()
            print("Despesas:")
            print()
            for despesa in cliente.despesas:
                print("  Categoria:", despesa.get_categoria())
                print("  Descrição:", despesa.get_descricao())
                print("  Valor:", despesa.get_valor())
                print("  Data:", despesa.get_data())
                print()
            current_node = current_node.next
    
    def print_list_cliente_despesas_orcamento(self):
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
            print()
            print("Despesas:")
            print()
            for despesa in cliente.despesas:
                print("  Categoria:", despesa.get_categoria())
                print("  Descrição:", despesa.get_descricao())
                print("  Valor:", despesa.get_valor())
                print("  Data:", despesa.get_data())
                print()
            print("Orçamento:")
            print()
            for orcamento in cliente.orcamento:
                print("  Orçamento:", orcamento.get_orcamento())
                print("  Gastos para o mês:", orcamento.get_gastos_mes())
                print()
            current_node = current_node.next