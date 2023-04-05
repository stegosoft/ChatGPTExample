def check_for_duplicate_links(path_to_new_content, links):
    '''
    檢查是否有重複的連結
    Parameters:
        path_to_new_content: 新內容的路徑
        links: 所有連結
    Return:
        True: 有重複的連結
        False: 沒有重複    '''
    urls = [str(link.get("href")) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls


def dataframe_to_database(df, table_name):
    '''
 將資料框架轉換成資料庫
 
 Parameters:
 df: 資料框架
 table_name: 資料表名稱
 
 Returns:
 engine: 資料庫引擎
    '''
    engine = create_engine(f'sqlite:///:memory:', echo=False)
    df.to_sql(name=table_name, con=engine, index=False)
    return engine


def execute_query(engine, query):
    '''
    功能: 執行 SQL 查詢
    參數: 
        engine: SQLAlchemy engine
        query: SQL 查詢
    回傳值: 查詢結果
    '''
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()


def grade(correct_answer_dict, answers):
    '''
    grade(correct_answer_dict, answers):
    功能: 
        根據答案字典及使用者答案，計算使用者答對題數及百分比，並判斷是否通過考    '''
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
    功能: 將 response 中的 query 加上 Select 字串
    參數: response (dict)
    回傳值: query (str)
    '''
    query = response["choices"][0]["text"]
    if query.startswith(" "):
        query = "Select"+ query
    return query
