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
repos = user.get_repos()
repo_name_list = []

for repo in repos:
    repo_name = repo.name    
    repo_name_list.append(repo.name)
print(f'Name of all repo in user {user.login} are:')       
index=0
while index < len(repo_name_list):
    print(f"{index}. {repo_name_list[index]}")
    index +=1
print(repo_name_list)    
select_repo = int(input("Enter index of repo:"))
selected_repo = g.get_repo(f"{user.login}/{repo_name_list[select_repo]}")
branches= list(selected_repo.get_branches())
for branch in branches:
    branch_name = branch.name
    commit = selected_repo.get_commit(sha=branch.commit.sha)
    commit_date = commit.commit.committer.date
    if commit_date.tzinfo is None:
        commit_date = commit_date.replace(tzinfo=timezone.utc)
    difference = checktimedelta(commit_date)

    if difference > timedelta(hours=staletime):
        if branch_name != 'main':
            branch_path = f"https://github.com/{user.login}/{repo_name}/{branch_name}"
            delete_branches.append(branch_path)

    branch_info_list.append({
        "repository": repo.name,

        "branch": branch_name,
        "date": commit_date ,
        "timedeltacheak": difference
    })
    print(difference)          




        

       