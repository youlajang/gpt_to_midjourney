import os
import io
import time
import warnings
import urllib.request
import json
import shutil
import openai
from openai import OpenAI
import streamlit as st


client = OpenAI(api_key= st.secrets["client"])
model="gpt-3.5-turbo"
role = "system"
role_content = "You are a skilled poetic assistant who uses your creative talents to create illustrative storybooks for children."



class Create_book: 
    def __init__(self, params,local_path):
        
        self.params = params
        self.local_path = local_path

    def create_story_text( story_prompt):

        story_prompt_command = f"Tell a short story  about : {story_prompt}. Please separate each paragraph with '\n\n'"
        response = client.chat.completions.create(
            model = model,
            messages=[
                        {"role": role, "content": role_content},
                        {"role": "user", "content": story_prompt_command}
                    ]
        )
        text = response.choices[0].message
        return text
    
    def transrate_text(text,n=None):
        trans_command = ''
        if n ==1 : 
            trans_command = f"Translate the following English text into Korean, but separate the sentences with an enter every 5 words: {text}"
        elif n ==2:
            trans_command = f"Please translate the following text from English to Korean at a level that even elementary school students can easily understand:{text}"
        
        response = client.chat.completions.create(
            model = model,
            messages=[
                        {"role": role, "content": role_content},
                        {"role": "user", "content": trans_command}
                    ]
        )
        text = response.choices[0].message.content
        text = text.replace("\n", "")
        return text

    def create_story_title(story_full_text):

        story_title_command = f"create an exciting, creative, clever, and short title for the following story that does not have quotes in it Choosing emotional words: ${story_full_text}"
        response = client.chat.completions.create(
            model = model,
            messages=[
                        {"role": role, "content": role_content},
                        {"role": "user", "content": story_title_command}
                    ]
        )
        
        text = response.choices[0].message.content
        text = text.replace("\n", "")
        return text

    
    def view_run(run_name):
        os.makedirs('./story-book/src/story', exist_ok=True)
        shutil.rmtree('./story-book/src/story')
        shutil.copytree(f'./story-book-runs/{run_name}', './story-book/src/story', dirs_exist_ok=True)

    ## run_name let's you keep the files generated for previous runs, it just places them in a folder named by the `run_name` param
    def create_story(run_name, story_prompt, art_style):
        
        os.makedirs('./story-book-runs/' + run_name, exist_ok=True)

        
        story_full_text = Create_book.create_story_text(story_prompt)
        story_title = Create_book.create_story_title(story_full_text)
        Create_book.view_run(run_name)
        return story_title, story_full_text

    def create_story_prompt(num_characters,characters_list,story):
        prompt = "Once upon a time, in a land far away"
        for character in characters_list:
            
            gender = character['성별']
            name = character['이름']
            
            if "남자" in gender:
                gender = "man"
                #pronoun = "He"
                face = "This man looks like Cha Eun-woo."
            elif "여자" in gender:
                gender = "woman"
                #pronoun = "She"
                face = "This woman resembles Korean actress Kim Yoo-jung."
            else:
                gender = "man"
                #pronoun = "He"
                face = "This man looks like Cha Eun-woo."
            
            prompt += f"Once lived a {gender} named {name}.{face}"
        
        
        # story = input("전체적으로 원하는 스토리를 작성해 주세요.: ")
        prompt += f"This story is about{story}. "

        story_prompt_command = f"{prompt} translate it to english"
        response = client.chat.completions.create(
            model = model,
            messages=[
                        {"role": role, "content": role_content},
                        {"role": "user", "content": story_prompt_command}
                    ]
        )
        prompt = response.choices[0].message
        print(prompt)
        return prompt




