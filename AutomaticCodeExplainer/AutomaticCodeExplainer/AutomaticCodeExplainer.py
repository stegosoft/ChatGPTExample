import os
from pyexpat import model
import openai
import inspect
import functions
import pathlib

openai.api_key = os.environ.get("OPEN_API_KEY")

def hello(name):
    print(f"Hello {name}")

def docstring_prompt_zh_tw(code):
    prompt = f"{code}\n # 幫 python function 使用中文加上程式碼說明，包含功能、參數以及回傳值，保留原本程式碼內容，所產內容每行都加上四個空白:\n '''"
    return prompt

def docstring_prompt(code):
    prompt = f"{code}\n # A high quality python docstring of the above python function, before ever row of docstring add 4 space:\n '''"
    return prompt

def merge_docstring_and_function_by_function_name(original_function, docstring):
    function_string = inspect.getsource(original_function)
    return merge_docstring_and_function(function_string, docstring)

def merge_docstring_and_function(code, docstring):
    function_string = code
    split = function_string.split('\n')
    first_part, second_part = split[0], split[1:]
    merged_function = f"{first_part}\n    '''{docstring.rstrip(' ')}    '''\n"+'\n'.join(second_part)
    return merged_function

def get_docstrings_by_function_name(docstring_prompt_function,function_name):
    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = docstring_prompt_function(inspect.getsource(function_name)),
        temperature =0,
        max_tokens = 100,
        top_p = 1.0,
        stop = ["'''"])
    print(merge_docstring_and_function_by_function_name(function_name,response['choices'][0]['text']))
    print('----------------------------')

def get_docstrings(docstring_prompt_function,code):
    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = docstring_prompt_function(code),
        temperature =0,
        max_tokens = 100,
        top_p = 1.0,
        stop = ["'''"])
    return response['choices'][0]['text']

def get_all_functions(module):
    return [mem for mem in inspect.getmembers(module, inspect.isfunction)
         if mem[1].__module__ == module.__name__]

all_functions = get_all_functions(functions)
#('check_for_duplicate_links', <function check_for_duplicate_links at 0x0000025B6E673670>)
#('dataframe_to_database', <function dataframe_to_database at 0x0000025B6DD97EE0>)
#('execute_query', <function execute_query at 0x0000025B6E63ECA0>)
#('grade', <function grade at 0x0000025B6E6735E0>)
#('handle_response', <function handle_response at 0x0000025B6DDA31F0>)
functions_with_docstrings=[]
functions_with_dotstrings_zh_tw=[]
for fun in all_functions:
    code =  inspect.getsource(fun[1])
    response = get_docstrings(docstring_prompt, code)
    merge_code = merge_docstring_and_function(code, response)
    functions_with_docstrings.append(merge_code)
    response_zh_tw = get_docstrings(docstring_prompt_zh_tw, code)
    merge_code_zh_tw = merge_docstring_and_function(code, response_zh_tw)
    functions_with_dotstrings_zh_tw.append(merge_code_zh_tw)

functions_to_prompt = functions
functions_to_prompt_name = pathlib.Path(functions_to_prompt.__file__).stem
with open(f"{functions_to_prompt_name}_withdocstring.py", "w") as f:
    f.write("\n\n".join(functions_with_docstrings))
with open(f"{functions_to_prompt_name}_withdocstring_zh_tw.py", "w") as f:
    f.write("\n\n".join(functions_with_dotstrings_zh_tw))

#get_docstrings(docstring_prompt_zh_tw, merge_docstring_and_function)
#get_docstrings(docstring_prompt, merge_docstring_and_function)