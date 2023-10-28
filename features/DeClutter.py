'''Our DeClutter AI Assistance'''
from constants.client_message import ERROR, TESTGENERATION
from features.ai_models.gpt3 import GPT3
from features.tasks.styleformer import StyleFormer
from utils.helpers import formate_output


class DeClutter:
    '''
    DeClutter AI Assistant
    selects the Task to perform according to input task.
    '''
    def __init__(self, feature, text_tone="professional") -> None:
        self.feature = feature
        self.text_tone = text_tone

    def execute(self, user_input_sequences, model) -> dict:

        text_tone = "As a " + self.text_tone

        if model == 'GPT3':
            model = GPT3(text_tone, self.feature.prompt, user_input_sequences)
        elif model == 'test':
            output = {'text': TESTGENERATION}
            return output
        else:
            output = ERROR
            return output

        output = model.generate()
        output['result'] = formate_output(output['result'])
        return output

    def styleformer(self, input_sequence, style=0):
        styleformer = StyleFormer(input_sequence, style)
        output = styleformer.transfer()

        return output
