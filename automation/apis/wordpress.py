'''Gpt J 6 billion based outputs'''

import openai
from django.conf import settings
import requests


class WordPress:
    '''
    WordPress
    core logic for WordPress Apis.
    '''

    def __init__(self, username, password, website) -> None:
        self.username = username
        self.password = password
        self.website = website

    def add_draft_post(self, title, content):
        """
        Adds Draft posts on wordpress
        """

        post_data = {
            'title': title,
            'content': content,
            'status': 'draft',
        }
        headers = {
            "Content-Type": "application/json"
        }
        auth = (self.username, self.password)
        api_url = f'https://{self.website}/wp-json/wp/v2/posts'

        response = requests.post(api_url, json=post_data, headers=headers, auth=auth)
        if response.status_code == 201:  # 201 indicates a successful creation
            response = response.json()
            return response['id']
        else:
            return f'Failed to create post. Status code: {response.status_code}'
    
    def update_post():
        pass
