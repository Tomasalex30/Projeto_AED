from model.Lista.Nodes import *
from model.Cliente import *
from view import *

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        new_node = DoubleNode(value)
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

    def remove(self, value):
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

    def print_list(self):
        current_node = self.head
        while current_node is not None:
            print("Nome:", current_node.value.get_nome())
            print("Password:", current_node.value.get_password())
            print("NIF:", current_node.value.get_nif())
            print()
            current_node = current_node.next