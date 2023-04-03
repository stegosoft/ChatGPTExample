import os
from pyexpat import model
import openai
import inspect

openai.api_key = os.environ.get("OPEN_API_KEY")

def hello(name):
    print(f"Hello {name}")

def docstring_prompt_zh_tw(code):
    prompt = f"{code}\n # 幫 python function 使用中文加上程式碼說明，包含功能、參數以及回傳值，保留原本程式碼內容:\n '''"
    return prompt

def docstring_prompt(code):
    prompt = f"{code}\n # A high quality python docstring of the above python function:\n '''"
    return prompt

def get_docstrings(docstring_prompt_function,function_name):
    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = docstring_prompt_function(inspect.getsource(function_name)),
        temperature =0,
        max_tokens = 100,
        top_p = 1.0,
        stop = ["'''"])
    print(response['choices'][0]['text'])
    print('----------------------------')

get_docstrings(docstring_prompt_zh_tw, hello)
get_docstrings(docstring_prompt, hello)