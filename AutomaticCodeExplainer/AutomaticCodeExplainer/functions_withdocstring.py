def check_for_duplicate_links(path_to_new_content, links):
    '''
    Checks for duplicate links in a given list of links.
    
    Parameters:
    path_to_new_content (Path): Path object of the new content.
    links (list): List of links to check for duplicates.
    
    Returns:
    bool: True if duplicate link is found, False otherwise.
    '''
    urls = [str(link.get("href")) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls


def dataframe_to_database(df, table_name):
    '''
    This function takes a dataframe and a table name as input and creates an in-memory sqlite database with the given table name and stores the dataframe in the table.
 
    Parameters:
    df (DataFrame): The dataframe to be stored in the database.
    table_name (str): The name of the table in the database.
 
    Returns:
    engine (Engine): The engine object of the created database.
    '''
    engine = create_engine(f'sqlite:///:memory:', echo=False)
    df.to_sql(name=table_name, con=engine, index=False)
    return engine


def execute_query(engine, query):
    '''
    Executes a query on a given engine and returns the result.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        The engine to execute the query on.
    query : str
        The query to execute.

    Returns
    -------
    list
        The result of the query.
    '''
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()


def grade(correct_answer_dict, answers):
    '''
    This function takes two arguments, a dictionary of correct answers and a dictionary of answers given by a student.
    It then compares the two dictionaries and returns a grade and a pass/fail message.
    Parameters:
        correct_answer_dict (dict): A dictionary of correct answers.
        answers (dict): A dictionary of answers given by a student.
    Returns:
        A string containing the grade and pass/fail message.
    '''
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


def handle_response(response):
    '''
    This function takes a response from a user and handles it.
    It takes the response as a parameter and returns a query.
    
    Parameters:
    response (dict): The response from the user.
    
    Returns:
    query (str): The query to be used.
    '''
    query = response["choices"][0]["text"]
    if query.startswith(" "):
        query = "Select"+ query
    return query
