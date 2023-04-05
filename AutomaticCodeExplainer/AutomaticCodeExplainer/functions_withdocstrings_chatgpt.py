from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import text
import numpy as np

"""
    Store a pandas DataFrame in a SQL database.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to be stored in a database.
    table_name (str): The name of the table that the DataFrame should be stored in.
    
    Returns:
    None
    """
def dataframe_to_database(df, table_name):
    engine = create_engine(f'sqlite:///:memory:', echo=False)
    df.to_sql(name=table_name, con=engine, index=False)
    return engine

"""
    Handle the response from a web request.

    Parameters:
    response (str): The response from a web request.

    Returns:
    dict: A dictionary containing the response data.
    """
def handle_response(response):
    query = response["choices"][0]["text"]
    if query.startswith(" "):
        query = "Select"+ query
    return query

"""
    Executes a given query on a given engine.

    Parameters
    ----------
    engine : object
        The engine to execute the query on.
    query : str
        The query to execute.

    Returns
    -------
    object
        The result of the query.
    """
def execute_query(engine, query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()

"""
    Calculate the grade of a student based on the correct answer to a question and their answer.

    Parameters:
    correct_answer_dict (dict): Dictionary of questions and their correct answer.
    answers (dict): Dictionary of questions and the student's answer.

    Returns:
    float: Grade as a percentage.
    """
def grade(correct_answer_dict, answers):
    correct_answers = 0
    for question, answer in answers.items():
        if answer.upper() == correct_answer_dict[question].upper()[16]:
            correct_answers+=1
    grade = 100 * correct_answers / len(answers)

    if grade < 60:
        passed = "Not passed!"
    else:
        passed = "Passed!"
    return f"{correct_answers} out of {len(answers)} correct! You achieved: {grade} % : {passed}"


"""
    Check for duplicate links in the given content.

    Parameters:
        path_to_new_content (str): Path to the new content to be checked.
        links (list): List of links to be checked.

    Returns:
        bool: True if duplicate links are found, False otherwise.
    """
def check_for_duplicate_links(path_to_new_content, links):
    urls = [str(link.get("href")) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls
