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
    # �d���ƪ��}�Y��m
    match = re.search(r"def\s+\w+\(", function_code)

    if match:
        # �b��ƶ}�Y���U�@�洡�Jdocstring
        index = match.end()
        indent = re.search(r"^\s*", function_code).group()  # �����e���Y��
        newline_index = function_code.find('\n', index) + 1  # �d�䴫��Ū���m
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

def add_string_to_filename(file_path, string_to_add):
    file_name, file_extension = os.path.splitext(file_path)
    new_file_name = f"{file_name}{string_to_add}{file_extension}"
    return new_file_name

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # �ϥΥ��h��F���d��Ҧ����
    functions = re.finditer(r"(def\s+\w+\()", content)

    # �f�ǳB�z�C�Ө�ơA�H�קK�b���Jdocstring�ɼv�T�����ƪ���m
    for match in reversed(list(functions)):
        start_index = match.start()
        end_index = content.find(":\n", start_index) + 1
        function_code = content[start_index:end_index]

        docstring = generate_docstring(function_code)
        updated_function_code = insert_docstring(function_code, docstring)

        # �N�ͦ���docstring���J���l�N�X��
        content = content[:start_index] + updated_function_code + content[end_index:]

    # �N��s�᪺�N�X�g�^���
    filename = add_string_to_filename(filepath, "_withdocstrings_chatgpt")
    with open(filename, "w") as f:
        f.write(content)

def insert_docstring_csharp(method_code, docstring):
    match = re.search(r"(\s+)(public|private|protected|internal)(\s+)", method_code)

    if match:
        indentation = match.group(1)
        docstring_lines = docstring.split("\n")
        indented_docstring = "\n".join([indentation + line for line in docstring_lines])
        updated_method_code = method_code.replace(match.group(0), f"{indentation}/// {indented_docstring}\n{match.group(0)}", 1)
        return updated_method_code
    else:
        return method_code

def process_csharp_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    methods = re.finditer(r"(public|private|protected|internal)\s+(static\s+)?\w+\s+\w+\s*\(.*\)\s*\{", content, flags=re.MULTILINE)

    for match in reversed(list(methods)):
        start_index = match.start()
        end_index = match.end()
        method_code = content[start_index:end_index]

        docstring = generate_docstring(method_code)
        updated_method_code = insert_docstring_csharp(method_code, docstring)

        content = content[:start_index] + updated_method_code + content[end_index:]

    filename = add_string_to_filename(filepath, "_withdocstrings_chatgpt")
    with open(filename, "w") as f:
        f.write(content)

method_code="""        static int Add(int a, int b)
        {
            return a + b;
        }"""

#print(generate_docstring(method_code))

# �N�H�U��������z�n�B�z��Python��󪺸��|
file_path = "csSampleCode.cs"
process_csharp_file(file_path)