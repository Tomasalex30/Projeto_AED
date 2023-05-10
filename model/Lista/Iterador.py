from abc import ABC

class ClientLinkedListIterator:
    def __init__(self, linked_list):
        self.linked_list = linked_list
        self.current_node = linked_list.head
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_node is None:
            raise StopIteration
        value = self.current_node.get_element()
        self.current_node = self.current_node.get_next_node()
        return value
