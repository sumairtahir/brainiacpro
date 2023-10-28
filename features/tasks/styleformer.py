import openai


class StyleFormer():
    '''style Former'''

    def __init__(self, input_sequence, style=0) -> None:
        self.input_sequence = input_sequence
        self.style = style

    def transfer(self) -> str:
        '''style formate selection'''
        if self.style == 0:
            output_sentence = self.casual()
            return output_sentence
        if self.style == 1:
            output_sentence = self.formal()
            return output_sentence
        if self.style == 2:
            output_sentence = self.active()
            return output_sentence
        if self.style == 3:
            output_sentence = self.passive()
            return output_sentence

        return self.input_sequence

    def casual(self):
        model_seq = "Convert this into Casual Voice tone:\n\n" +\
            self.input_sequence

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=model_seq,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response

    def formal(self):
        model_seq = "Conver this into Casual Voice tone:\n\n" +\
            self.input_sequence

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=model_seq,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response

    def active(self):
        model_seq = "Conver this into Casual Voice tone:\n\n" +\
            self.input_sequence

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=model_seq,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response

    def passive(self):
        model_seq = "Conver this into Casual Voice tone:\n\n" +\
            self.input_sequence

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=model_seq,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response
