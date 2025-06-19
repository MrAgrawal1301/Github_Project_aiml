from github import Github , Auth
import json
from mrkdwn_analysis import MarkdownAnalyzer

auth = Auth.Token('')
g = Github(auth = auth)
user = g.get_user()
repos = user.get_repos()
for repo in repos: 
    prs = repo.get_pulls()
    index = 1
    for pr in prs:
        if pr.body:
            text = pr.body
            with open('my_file.txt', 'w') as file:
                file.write(text)
            analyzer = MarkdownAnalyzer("my_file.txt")
            list = analyzer.identify_task_items()
            print(list)
            description_detail = {
                'title of pr': pr.title,
                'repo name': repo.name,
                'description': list
            }
            print(f'{index} , {json.dumps(description_detail , indent=4)}')
            print('============================================================================================')
    for pr in prs:
        comments = pr.get_issue_comments() 
        for comment in comments:
            info = {
                'user_to comment': comment.user.login,
                'comment_time': comment.created_at.ctime(),
                'body': comment.body,
                'title of pr': pr.title,
                'repo name': pr.head.repo.name,
                'branch from where pr generated': pr.head.ref
            }
            print(f'{index}. {json.dumps(info , indent=4)} ')
            index += 1

        
