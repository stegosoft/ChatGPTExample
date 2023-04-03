import os
from pyexpat import model
import openai
import inspect

openai.api_key = os.environ.get("OPEN_API_KEY")

def hello(name):
    print(f"Hello {name}")

def docstring_prompt_zh_tw(code):
    prompt = f"{code}\n # 幫 python function 使用中文加上程式碼說明，包含功能、參數以及回傳值，保留原本程式碼內容，所產內容每行都加上四個空白:\n '''"
    return prompt

def docstring_prompt(code):
    prompt = f"{code}\n # A high quality python docstring of the above python function, before ever row of docstring add 4 space:\n '''"
    return prompt

def merge_docstring_and_function(original_function, docstring):
    function_string = inspect.getsource(original_function)
    split = function_string.split('\n')
    first_part, second_part = split[0], split[1:]
    merged_function = f"{first_part}\n    '''{docstring.rstrip(' ')}    '''\n"+'\n'.join(second_part)
    return merged_function

def get_docstrings(docstring_prompt_function,function_name):
    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = docstring_prompt_function(inspect.getsource(function_name)),
        temperature =0,
        max_tokens = 100,
        top_p = 1.0,
        stop = ["'''"])
    print(merge_docstring_and_function(function_name,response['choices'][0]['text']))
    print('----------------------------')



get_docstrings(docstring_prompt_zh_tw, merge_docstring_and_function)
get_docstrings(docstring_prompt, merge_docstring_and_function)