def check_for_duplicate_links(path_to_new_content, links):
    '''
    �ˬd�O�_�����ƪ��s��
    Parameters:
        path_to_new_content: �s���e����|
        links: �Ҧ��s��
    Return:
        True: �����ƪ��s��
        False: �S������    '''
    urls = [str(link.get("href")) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls


def dataframe_to_database(df, table_name):
    '''
 �N��Ʈج[�ഫ����Ʈw
 
 Parameters:
 df: ��Ʈج[
 table_name: ��ƪ�W��
 
 Returns:
 engine: ��Ʈw����
    '''
    engine = create_engine(f'sqlite:///:memory:', echo=False)
    df.to_sql(name=table_name, con=engine, index=False)
    return engine


def execute_query(engine, query):
    '''
    �\��: ���� SQL �d��
    �Ѽ�: 
        engine: SQLAlchemy engine
        query: SQL �d��
    �^�ǭ�: �d�ߵ��G
    '''
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()


def grade(correct_answer_dict, answers):
    '''
    grade(correct_answer_dict, answers):
    �\��: 
        �ھڵ��צr��ΨϥΪ̵��סA�p��ϥΪ̵����D�ƤΦʤ���A�çP�_�O�_�q�L��    '''
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
    �\��: �N response ���� query �[�W Select �r��
    �Ѽ�: response (dict)
    �^�ǭ�: query (str)
    '''
    query = response["choices"][0]["text"]
    if query.startswith(" "):
        query = "Select"+ query
    return query
