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
    # 琩тㄧ计秨繷竚
    match = re.search(r"def\s+\w+\(", function_code)

    if match:
        # ㄧ计秨繷︽础docstring
        index = match.end()
        indent = re.search(r"^\s*", function_code).group()  # 莉讽玡罽逼
        newline_index = function_code.find('\n', index) + 1  # 琩т传︽才竚
        updated_function_code = (
            function_code[:newline_index]
            + indent
            + docstring.replace("\n", f"\n{indent}")
            + "\n"
            + function_code[newline_index:]
        )
        return updated_function_code
    else:
        return function_code

function_code = """def add(a, b):
    return a + b"""

docstring = generate_docstring(function_code)

updated_function_code = insert_docstring(function_code, docstring)
print(updated_function_code)

#def add(a, b):
#"""
#    This function adds two numbers and returns the result.

#    Parameters:
#    a (int): The first number to add.
#    b (int): The second number to add.

#    Returns:
#    int: The result of the addition.
#"""
#    return a + b