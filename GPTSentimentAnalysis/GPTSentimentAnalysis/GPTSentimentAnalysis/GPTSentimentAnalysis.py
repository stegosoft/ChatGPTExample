
from turtle import pos
import openai
import os
import praw

client_id = os.environ.get("REDDIT_CLIENT_ID")
client_key = os.environ.get("REDDIT_CLIENT_SECRET")
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_key,
                     user_agent='sentiment analysis test')

def get_titles_and_comments(subreddit_name="stocks", limit =6, num_comments =3, skip_first=2):
    subreddit = reddit.subreddit(subreddit_name)
    title_and_comments = {}

    for counter, post in enumerate(subreddit.hot(limit=limit)):
        if counter < skip_first:
            continue
        counter += (1-skip_first)
        title_and_comments[counter] = ""
        #PRAW 
        submission = reddit.submission(post.id)
        title = post.title
        title_and_comments[counter] += "Title: "+ title +"\n\n"
        title_and_comments[counter] += "Comments: \n\n"

        comment_counter = 0
        for comment in submission.comments:
            if not comment.body == "[deleted]":
                title_and_comments[counter]+= comment.body+"\n"
                comment_counter +=1
            if comment_counter == num_comments:
                break
    return title_and_comments

def create_prompt(title_and_comments):
    task = "在後續的標題與內文中分析，並返回股票代碼或公司名稱並告知該則消息是正面、反面或者是中性，如果沒有提到公司名稱，則註記沒有指定公司名稱\n\n"
    return task+title_and_comments

title_and_comments =get_titles_and_comments()
openai.api_key = os.environ.get("OPEN_API_KEY")
for key, title_with_comments in title_and_comments.items():
    prompt = create_prompt(title_with_comments)
    response = openai.Completion.create(engine = "text-davinci-003",
                                        prompt = prompt,
                                        max_tokens = 256,
                                        temperature=0,
                                        top_p = 1.0)
    print(title_with_comments)
    responseText = response['choices'][0]["text"]
    print(f"情緒報告(openAI): {responseText}")
    print("--------------------------------------------")