import openai
from termcolor import colored
import streamlit as st

from config import CHAT_MODEL, COMPLETIONS_MODEL, INDEX_NAME

# A basic class to create a message as a dict for chat
class Message:
    
    def __init__(self, role,content):
        self.role = role
        self.content = content
        
    def message(self):
        return {
            "role": self.role,
            "content": self.content
        }

# New Assistant class to add a vector database call to its responses
class RetrievalAssistant:
    
    def __init__(self):
        self.conversation_history = []  

    def _get_assistant_response(self, prompt):
        try:
            completion = openai.ChatCompletion.create(
              model=CHAT_MODEL,
              messages=prompt,
              temperature=0.1
            )
            
            response_message = Message(
                completion['choices'][0]['message']['role'],
                completion['choices'][0]['message']['content']
            )
            return response_message.message()
            
        except Exception as e:

            return f'Request failed with exception {e}'
      
    def ask_assistant(self, next_user_prompt):
        [self.conversation_history.append(x) for x in next_user_prompt]
        assistant_response = self._get_assistant_response(self.conversation_history)
        self.conversation_history.append(assistant_response)
        return assistant_response
            
    def pretty_print_conversation_history(
            self, 
            colorize_assistant_replies=True):
        
        for entry in self.conversation_history:
            if entry['role']=='system':
                pass
            else:
                prefix = entry['role']
                content = entry['content']
                if colorize_assistant_replies and entry['role'] == 'assistant':
                    output = colored(f"{prefix}:\n{content}, green")
                else:
                    output = colored(f"{prefix}:\n{content}")
                print(output)
