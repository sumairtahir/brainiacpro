'''Abstact Task class'''

from abc import abstractmethod


class Task:
    '''Abstract functions to perform by selected task.'''

    def __init__(self, input_sequence) -> None:
        self.input_sequence = input_sequence

    @abstractmethod
    def generate(self) -> dict:
        '''this will generate the output w.r.t selected Model'''

    @abstractmethod
    def select_model(self) -> str:
        '''this will select the model.'''
