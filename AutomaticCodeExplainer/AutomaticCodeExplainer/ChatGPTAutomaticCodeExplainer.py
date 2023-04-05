import openai
import os
import re

openai.api_key = os.environ.get("OPEN_API_KEY")

def generate_docstring(function_code):
    prompt = f"Write a high quality docstring for the following Python function, parameter and return with new line and all lines offset 4 space:\n\n{function_code}\n\nDocstring:\n"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    docstring = response.choices[0].text.strip()
    return docstring


def insert_docstring(function_code, docstring):
    # 查找函數的開頭位置
    match = re.search(r"def\s+\w+\(", function_code)

    if match:
        # 在函數開頭的下一行插入docstring
        index = match.end()
        updated_function_code = function_code[:index] + "\n    " + docstring.replace("\n", "\n    ") + "\n" + function_code[index:]
        return updated_function_code
    else:
        return function_code

function_code = """def add(a, b):
    return a + b"""

docstring = generate_docstring(function_code)

updated_function_code = insert_docstring(function_code, docstring)
print(updated_function_code)
