


class Task:
    '''
    Abstract functions to perform by selected task.
    '''
    def __init__(self, input_sequence) -> None:
        self.input_sequence = input_sequence

    @abstractmethod
    def generate(self) -> dict:
        '''this will generate the output'''

    @abstractmethod
    def select_model(self) -> str:
        '''
        this will select the model and generate
        output according to the selected model
        '''
        pass