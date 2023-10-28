'''Gpt J 6 billion based outputs'''

import openai
import requests
from django.conf import settings
from constants.client_message import ERROR, TESTGENERATION

openai.api_key = settings.OPENAIKEY

headers = {
  "Authorization": "Bearer " + settings.FOREFRONT1,
  "Content-Type": "application/json"
}

class GPTJ:
    '''gpt j'''

    def __init__(self, task, input_sequence) -> None:
        self.task = task
        self.input_sequence = input_sequence

    def generate(self):
        '''This is going to run the selected task for the model.'''

        if self.task == 'TS':
            output = self.text_simplification(self.input_sequence)
        elif self.task == 'TSum':
            output = self.text_summerization(self.input_sequence)
        elif self.task == 'Para':
            output = self.text_paraphrasing(self.input_sequence)
        elif self.task == 'test':
            output = TESTGENERATION
        else:
            output = ERROR
        return output

    def text_simplification(self, input_sequence):
        '''
        Text Simplification using GPT J 6b parameter Model
        trained on text simplified data set, Deployed on
        Forefront
        '''
        input_sequence = "Summarize this for a second-grade student:\n\n" +\
            input_sequence

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
        print(response)
        output['result'] = response['choices'][0]['text']
        output['usage'] = response['usage']
        print("output")
        return output
    

    def text_summerization(self, input_sequence):
        '''
        Text Simplification using GPT J 6b parameter Model
        trained on text simplified data set, Deployed on
        Forefront
        '''
        body = {
            "compression_level": 5,
            "text": input_sequence
        }

        res = requests.post(
            "https://solutions.forefront.ai/v1/organization/9mVMD3157sFg/summarize",
            json=body,
            headers=headers,
            timeout=60
        )

        response = res.json()
        output = {}
        output['result'] = response['summary']
        return output
    
    def text_paraphrasing(self, input_sequence):
        '''
        Text Simplification using T5 20b parameter Model
        trained on text simplified data set, Deployed on
        Forefront
        '''
        input_sequence = "paraphrase the following:\n\n" +\
            input_sequence

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

        return output

