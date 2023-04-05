from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import text
import numpy as np

"""
    Store a pandas DataFrame in a SQL database.
    
    Parameters:
    df (pandas.DataFrame): DataFrame to store in the database.
    table_name (str): Name of the table to store the DataFrame.
    
    Returns:
    None
    """
def dataframe_to_database(df, table_name):
    engine = create_engine(f'sqlite:///:memory:', echo=False)
    df.to_sql(name=table_name, con=engine, index=False)
    return engine

"""
    Handle an API response and return the data.

    Parameters
    ----------
    response : dict
        The response from an API call.

    Returns
    -------
    data : dict
        The data contained in the response.
    """
def handle_response(response):
    query = response["choices"][0]["text"]
    if query.startswith(" "):
        query = "Select"+ query
    return query

"""
    Executes a SQL query on the given engine.

    Parameters:
    engine (object): The engine to execute the query on.
    query (str): The SQL query to execute.

    Returns:
    object: The result of the query.
    """
def execute_query(engine, query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()

"""
    Calculate the grade of a student based on their answers to a set of questions.
    
    Parameters:
        correct_answer_dict (dict): Dictionary containing the correct answer for each question.
        answers (dict): Dictionary containing the student's answers to each question.
    
    Returns:
        float: The student's grade, represented as a float between 0 and 1.
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
    Checks for duplicate links in a file of new content.
    
    Parameters:
    path_to_new_content (str): The path to the file containing the new content.
    links (list): A list of links to check for duplicates.
    
    Returns:
    bool: True if duplicate links are found, False otherwise.
    """
def check_for_duplicate_links(path_to_new_content, links):
    urls = [str(link.get("href")) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls
