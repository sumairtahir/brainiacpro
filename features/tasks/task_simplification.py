'''ALL ABOUT TEXT SIMPLIFICATION'''
from features.ai_models.gpt_J import GPTJ
from features.tasks.Task import Task


class TextSimplification(Task):
    '''Text simplification'''
    def __init__(self, input_sequence, model) -> None:
        super().__init__(input_sequence)
        self.model = model

    def generate(self) -> dict:
        model = self.select_model()
        output = model.generate()

        return output

    def select_model(self):
        if self.model == 'gpt_j':
            model = GPTJ('TS', self.input_sequence)

        return model
