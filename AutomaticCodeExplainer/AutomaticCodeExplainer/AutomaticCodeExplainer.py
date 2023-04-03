import os
from pyexpat import model
import openai
import inspect

openai.api_key = os.environ.get("OPEN_API_KEY")

def hello(name):
    print(f"Hello {name}")

def docstring_prompt(code):
    prompt = f"{code}\n # 幫 python function 使用中文加上程式碼註解:\n '''"
    return prompt

response = openai.Completion.create(
    model = 'code-davinci-002',
    prompt = docstring_prompt(inspect.getsource(hello)),
    temperature =0,
    max_tokens = 100,
    top_p = 1.0,
    stop = ["'''"])
print(response['choices'][0]['text'])