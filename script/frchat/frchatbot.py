import openai
import yaml
import os

class FRChatBot(object):
    """
        A ChatBot generating command to control FR Cobots

        Author: wangyan
        Date: 2023/05/04

         A ChatBot generating command to control FR Cobots limit
         Author:Shujian
         Date:2023/05/09
    """
    
    def __init__(self, 
                 messages, 
                 temperature=0.3, 
                 model="gpt-3.5-turbo") -> None:
        self.messages = messages
        self.temperature = temperature  # this is the degree of the randomness of the response
        self.model = model
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def get_completion_from_messages(self, messages, temperature, model):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        # print(str(response.choices[0].message))
        return response.choices[0].message["content"]

    def build_message(self, role, content):
        message = {'role':role, 'content':content}
        return message

    def chat(self, prompt):
        print(f"USER:{prompt}\n==========\n")
        self.messages.append(self.build_message('user', prompt))
        response = self.get_completion_from_messages(messages=self.messages, 
                                                     temperature=self.temperature,
                                                     model=self.model)
        print(f"FR:{response}")
        self.messages.append(self.build_message('assistant', response))
        return response

    def generate_function_list(self, file):
        """
            Reading function infos from a YAML file
        """
        with open(file, "rb") as f:
            functions = yaml.safe_load(f)
        def read_function(func):
            func_name = func['name']
            args = ", ".join(arg['name'] for arg in func['arguments'])
            desc = func['description']
            arg_desc = ", ".join(f"{arg['name']}:{arg['description']}({arg['type']}型变量)" for arg in func['arguments'])
            ret = func['return']
            return [f"{func_name}", f"功能:'{desc}'", f"参数:'{arg_desc}'", f"返回值:'{ret}'"]
        output = [read_function(func['function']) for func in functions]
        return output