'''T5 20 billion based outputs'''
from django.conf import settings
import requests
from constants.client_message import TESTGENERATION


headers = {
  "Authorization": "Bearer " + settings.FOREFRONT1,
  "Content-Type": "application/json"
}


class T5:
    '''T5 20b'''
    def __init__(self, task, input_sequence) -> None:
        self.task = task
        self.input_sequence = input_sequence

    def generate(self):
        '''This is going to run the selected task for the model.'''

        output = 'this is a test text simplification for no match'
        if self.task == 'TS':
            output = self.text_simplification(self.input_sequence)
        elif self.task == 'Para':
            output = self.text_paraphrasing(self.input_sequence)
        elif self.task == 'test':
            output = TESTGENERATION
        return output

    def text_simplification(self, input_sequence):
        '''
        Text Simplification using T5 20b parameter Model
        trained on text simplified data set, Deployed on
        Forefront
        '''
        body = {
                "text": input_sequence,
                "top_p": 1,
                "top_k": 40,
                "temperature": 0.8,
                "repetition_penalty":  1,
                "length": 64
            }
        response = requests.post(
            "https://shared-api.forefront.link/organization/9mVMD3157sFg/gpt-j-6b-vanilla/completions/daijSFsVH8Yb",
            json=body,
            headers=headers,
            timeout=5000,
            )
        response = response.json()
        output = {}
        output['result'] = response['result'][0]['completion']

        return output
    
    def text_paraphrasing(self, input_sequence):
        '''
        Text Simplification using T5 20b parameter Model
        trained on text simplified data set, Deployed on
        Forefront
        '''
        body = {
            "text": "[S2S] Paraphrase the following text.\nText: " + input_sequence + " Paraphrased text: <extra_id_0>",
            "top_p": 0.5,
            "top_k": 40,
            "temperature": 1,
            "repetition_penalty":  1,
            "length": 96
        }

        res = requests.post(
            "https://shared-api.forefront.link/organization/9mVMD3157sFg/t5-20b/completions/KZV0705nNGoL",
            json=body,
            headers=headers,
            timeout=60
        )
        response = res.json()
        print(response)
        output = {}
        output['result'] = response['result'][0]['completion']

        return output
    

