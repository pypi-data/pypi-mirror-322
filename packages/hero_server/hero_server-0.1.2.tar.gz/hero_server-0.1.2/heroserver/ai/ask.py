import os
import json
import enum
import textwrap
from typing import List, Optional
import logging
from termcolor import colored

import ollama
import openai
from openai import OpenAI
from ai.instruction import instructions_load, instructions_get, instructions_reset

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class Model(enum.Enum):
    QWEN72I = "Qwen/Qwen2-72B-Instruct"
    MIXTRAL7I = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    PHI3_MEDIUM = "phi3:medium-128k"
    PHI3_MINI = "phi3:mini"    
    GPT35 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    GPT4O = "gpt-4o"
    QWEN1L= "qwen2:1.5b" #local
    QWEN0L= "qwen2:0.5b" #local
    PHI3L = "phi3:3.8b"
    QWEN7L= "qwen2:7b" #local

class AIAssistant:
    def __init__(self):
        self.model = Model.QWEN72I
        self.openai_client = None
        self.deepinfra_client = None
        self._setup_clients()

    def _setup_clients(self):
        openaikey = os.getenv("OPENAIKEY")
        if openaikey:
            logger.info(colored("OpenAI key set", "green"))
            openai.api_key = openaikey
            self.openai_client = openai

        deepinfrakey = os.getenv("DEEPINFRAKEY")
        if deepinfrakey:
            logger.info(colored("DEEPINFRAKEY key set", "green"))
            self.deepinfra_client = OpenAI(
                api_key=deepinfrakey,
                base_url="https://api.deepinfra.com/v1/openai",
            )

    def set_model(self, model: Model):
        self.model = model
        logger.info(colored(f"Model set to: {model.value}", "cyan"))

    def ask(self, question: str, category: str = "", name: str = "", log: bool = True) -> str:
        logger.info(colored(f"Asking question in category: {category}, name: {name}", "yellow"))
        mm = instructions_get(category=category, name=name)        
        mm.add_message(role="user", content=question)
        #mm.print_messages()

        if self.model in [Model.GPT4O, Model.GPT4, Model.GPT35]:
            response = self._ask_openai(mm.messages, log)
        elif self.model in [Model.QWEN72I, Model.MIXTRAL7I]:
            response = self._ask_deepinfra(mm.messages, log)
        else:            
            response = self._ask_ollama(mm.messages, log)

        logger.info(colored("Ask completed", "green"))
        return response

    def _ask_openai(self, messages, log: bool) -> str:
        response = self.openai_client.chat.completions.create(
            model=self.model.value,
            messages=messages,
            max_tokens=300
        )
        r = response.choices[0].message.content
        if log:
            logger.info(colored(f"OpenAI Response: {self.model.value}", "magenta"))
            logger.info(colored(r, "white"))
        return r

    def _ask_ollama(self, messages, log: bool) -> str:
        response = ollama.chat(model=self.model.value, messages=messages)
        if log:
            logger.info(colored(response['message']['content'], "white"))
        return response['message']['content']

    def _ask_deepinfra(self, messages, log: bool) -> str:
        chat_completion = self.deepinfra_client.chat.completions.create(
            model=self.model.value,
            messages=messages,
            max_tokens=None,
            stream=False
        )
        
        if log:
            logger.info(colored(f"\nDeepInfra Response: {self.model.value}", "magenta"))
            logger.info(colored("-" * 20, "white"))
            logger.info(colored(chat_completion.choices[0].message.content, "white"))
            logger.info(colored("\nToken Usage:", "cyan"))
            logger.info(colored(f"Prompt tokens: {chat_completion.usage.prompt_tokens}", "white"))
            logger.info(colored(f"Completion tokens: {chat_completion.usage.completion_tokens}", "white"))

        return chat_completion.choices[0].message.content
    
    
def ai_assistent(reset:bool=True) -> AIAssistant:
    mypath="~/code/git.ourworld.tf/projectmycelium/hero_server/lib/ai/instructions"
    if reset:
        instructions_reset()
    instructions_load(mypath)    
    return AIAssistant()

# Usage example:
if __name__ == "__main__":
    
    mypath="~/code/git.ourworld.tf/projectmycelium/hero_server/lib/ai/instructions"
    instructions_reset()
    instructions_load(mypath)    
    
    assistant = AIAssistant()
    
    #assistant.set_model(Model.MIXTRAL7I)  # Or any other model you prefer
    assistant.set_model(Model.QWEN72I)
    #assistant.set_model(Model.PHI3L)

    # response = assistant.ask(
    #     category='timemgmt',
    #     name='schedule',
    #     question='''
    #     lets create a story
        
    #     we need to paint our church
        
    #     its long over due, the major complained, 
    #     and his mother isn't happy
        
    #     oh yes I forgot its election time
        
    #     tom and ben will own this story
    #     its for our church in zanzibar

    #     we need to do it in 4 month from now    
        
    #     our requirements are:
        
    #     we need to make sure it can withstand sun
    #     color is white
    #     cost below 1000 USD
    #     '''
    # )
    #logger.info(colored("Final Response:", "green"))
    
    
    response = assistant.ask(
        category='',
        name='',
        question='''
        
        based on following names [Isabelle, Kristof, Jan, Rob, Florine, Florian, Sabrina, Tom, Ben]
        
        - find the owners of the story out of the text below, these owners are the ones who will do the task
        - see if these names are in the list above
        - if names match, return them, if not give error
        - return the names as a json list, don't give any other output
        
        ------

        
        we need to paint our church
        
        its long over due, the major complained, 
        and his mother isn't happy
        
        oh yes I forgot its election time
        
        tom and ben will own this story
        its for our church in zanzibar

        we need to do it in 4 month from now    
        
        our requirements are:
        
        we need to make sure it can withstand sun
        color is white
        cost below 1000 USD
        
        '''
    )   
    
    
    logger.info(colored(response, "white"))