import os 
from github import Github 
from datetime import timezone , datetime , timedelta
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
g = Github(token)
user = g.get_user()
print(f'The Authenticated user is {user.login}')
repos = user.get_repos()
for repo in repos:
        contributes = repo.get_contributors()
        commisions = repo.get_commits()
        for commit in commisions:
            print(commit.commit.committer.date)
        branches = repo.get_branches()
        prs = repo.get_pulls()
        for branch in branches:
            for contributer in contributes:
                print(f'Contributor: {contributer.login} made {contributer.contributions} commits to repository {repo.name} in branch ({branch.name})')
