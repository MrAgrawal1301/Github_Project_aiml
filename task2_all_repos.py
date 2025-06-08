import os
from datetime import datetime, timedelta, timezone 
from dotenv import load_dotenv
load_dotenv()
from github import Github
token  = os.getenv("GITHUB_TOKEN")

# Public Web Github
g = Github(token)
staletime = int(input("Enter No. of Hours:"))
    

def checktimedelta(timestamp):
    """Returns the time difference between now and the given timestamp."""
    now = datetime.now(timezone.utc)
    difference = now - timestamp
    return difference

user = g.get_user()
print(f"User Name is: {user.login}")
branch_info_list = []
delete_branches = []
grouped_list = []
repos = user.get_repos()
repo_name_list = []

for repo in repos:
    repo_name = repo.name    
    repo_name_list.append(repo.name)
    branches= repo.get_branches()
    repos_stale_branch = []
    for branch in branches:
        branch_name = branch.name
        commit = repo.get_commit(sha=branch.commit.sha)
        commit_date = commit.commit.committer.date 
        if commit_date.tzinfo is None:
            commit_date = commit_date.replace(tzinfo=timezone.utc)
        difference = checktimedelta(commit_date)

        if difference > timedelta(hours=staletime):
            if branch_name != 'main':
                branch_path = f"https://github.com/{user.login}/{repo_name}/{branch_name}"
                delete_branches.append(branch_path)
                repos_stale_branch.append(branch_path)

        branch_info_list.append({
            "repository": repo.name,
            "branch": branch_name,
            "date": commit_date ,
            "timedeltacheak": difference
        })     

        if branch_name =='main':
            commit_authur = commit.author
            author_name = commit_authur.login
            grouped_list.append({
                "repo name" :repo_name,
                "Author of the Main":author_name,
                "Path of the branch that are stale":repos_stale_branch
            })

for i in grouped_list:
    print(i)      



            

        