import os 
from github import Github
from datetime import datetime , timezone , timedelta
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('GITHUB_TOKEN')

g = Github(token)
user =g.get_user()
repos = user.get_repos()
print('The Authenticated User is:',user.login)

try:
    stale_threshold_hours = int(input("Enter the number of hours to define a stale branch: "))
except ValueError:
    print("Invalid input. Please enter a valid number.")

def cheak_time_delta(timestamp):
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo = timezone.utc)
    now = datetime.now(timezone.utc)
    difference = now - timestamp
    return difference

def get_risk_score(stale_time):
    risk_score = {
        "Low Risk": 3,
        "Medium Risk": 5,
        "High Risk": 8,
        "Critical Risk": 10,
    }
    level_of_risk = None
    for a,b in risk_score.items():
        if stale_time<b:
            level_of_risk = f"{a} --> The Stale branch is {stale_time} days old"
            break
        else:
            level_of_risk = f"Critical Risk --> The Stale branch is {stale_time} days old"   
    return level_of_risk 
 
def main():
    index = 1  
    for repo in repos:
        repo_name = repo.name 
        branches = repo.get_branches()
        for branch in branches:
            if branch.name != 'main':    
                branch_name = branch.name
                commit = repo.get_commit(sha=branch.commit.sha)
                commit_date = commit.commit.committer.date 
                difference = cheak_time_delta(commit_date)
                if difference > timedelta(hours=stale_threshold_hours):
                    stale_branch_url = f"https://github.com/{user.login}/{repo_name}/tree/{branch_name}"
                    difference_days = difference.days
                    risk_score = get_risk_score(difference_days)
                    commit_author = commit.author
                    author_name = commit_author.login if commit_author else "Unknown"
                    print(f'{index}. [Repo Name: {repo_name},\n Stale Branch url: {stale_branch_url},\n Author Name of Branch: {author_name},\n Last commit is ({difference}) old],\n Risk Level: {risk_score}]')
                    index += 1  
                             
if __name__ == '__main__':
    main()