'''Gpt J 6 billion based outputs'''

import openai
from django.conf import settings
from constants.client_message import ERROR, TESTGENERATION

openai.api_key = settings.OPENAIKEY

headers = {
    "Authorization": "Bearer " + settings.FOREFRONT1,
    "Content-Type": "application/json"
}


class GPT3:
    '''
    OPENAI GPT3
    core logic for text completion.
    '''
    TEXT = 1
    IMAGE = 2

    def __init__(self, writing_style_sequence, task_input_sequence, user_input_sequences) -> None:
        self.task_input_sequence = task_input_sequence.format(**user_input_sequences)
        self.writing_style_sequence = writing_style_sequence

    def generate(self, mode):
        '''This is going to run the selected task for the model.'''

        output = {}
        output['result'] = TESTGENERATION

        if settings.IS_PRODUCTION:
            try:
                if mode == self.TEXT:
                    output = self.generate_text(self.writing_style_sequence, self.task_input_sequence)
                elif mode == self.IMAGE:
                    output = self.generate_image(self.task_input_sequence)
                
            except Exception:
                output = ERROR

        return output
    
    def generate_image(image_prompt):
        '''
        Image Generation using openai GPT3 model api.
        **parameters**
        - image_prompt = holds the input string
          for letting gpt3 know what to do.
        '''

        try:
            response = openai.Completion.create(
                engine="image-alpha-001",  # Use the appropriate DALL·E engine
                prompt=image_prompt,
                max_tokens=200,  # Adjust as needed
                n=1,  # Number of images to generate
            )

            output = {}
            output['result'] = response.choices[0].image
        except Exception as exception:
            print(exception)
            output = {}
            output['result'] = ""
            output['usage'] = 0
            output['error'] = "Something went wrong."

        return output

    def generate_text(self, writing_style_sequence, task_input_sequence):
        '''
        Text Completion using openai GPT3 model api.
        **parameters**
        - writing_style_sequence lets GPT3 know to
          in which writing style it should write.

        - task_input_sequence = holds the input string
          for letting gpt3 know what to do with the user_input_sequence.
        '''

        input_sequence = writing_style_sequence + " " + task_input_sequence

        try:
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=input_sequence,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            output = {}
            output['result'] = response['choices'][0]['text']
        except Exception as exception:
            print(exception)
            output = {}
            output['result'] = ""
            output['usage'] = 0
            output['error'] = "Something went wrong."

        return output
