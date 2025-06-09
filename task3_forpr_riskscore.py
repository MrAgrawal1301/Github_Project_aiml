import os 
from github import Github
from datetime import datetime , timedelta , timezone
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
g = Github(token)
user = g.get_user()
print(f'The Authenticated user is {user.login}')

def check_timedelta(timestamp):
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo = timezone.utc)
    now = datetime.now(timezone.utc)
    difference = now - timestamp
    return difference 

def get_risk_score(created_day):
    risk_score = {
        "Low Risk": 3,
        "Medium Risk": 5,
        "High Risk": 8,
        "Critical Risk": 10,
    }
    level_of_risk = None
    for a,b in risk_score.items():
        if created_day < b:
            level_of_risk = f'{a} --> The PR is created {created_day} days ago.'
            break
        else:
            level_of_risk = f'Critical Risk --> The PR is created {created_day} days ago.'
    return level_of_risk

def main():
    index = 1
    repos = user.get_repos()
    for repo in repos:
        repo_name = repo.name
        prs = repo.get_pulls(state='all')
        for pr in prs:
            filebook = []
            commitbook = []
            created_time = pr.created_at
            time_difference_from_created_date = check_timedelta(created_time)
            difference_createdat_in_days = time_difference_from_created_date.days
            risk_level = get_risk_score(difference_createdat_in_days)
            files =pr.get_files()
            for file in files:
                filebook.append(file.filename)
            commits = pr.get_commits()  
            for commit in commits:
                dateis = commit.commit.committer.date
                difference = check_timedelta(dateis)
                commitbook.append(difference)
            timeoffrequancy = 1    
            freqancy = 'Not Enough Data'
            if len(commitbook) > 1:
                for i in range(len(commitbook) - 1):
                    diff = commitbook[i + 1] - commitbook[i]
                    if diff < timedelta(minutes=timeoffrequancy):
                        freqancy = 'Consistent'
                        break
                    else:
                        freqancy = 'Inconsistent'
        
            pr_details = f"[Repo Name: {repo_name} | PullRequest: {pr.title} | Number of commits: {pr.commits} |{freqancy} | Author: {pr.user.login} | State: {pr.state} | Created at: {pr.created_at} | Seen at: {pr.closed_at} |Risk Level: {risk_level} | Merge Date: {pr.merged_at} | Merged by: {pr.merged_by} | When the pr was again updated: {pr.updated_at} | Files in which changes were done: {filebook}]"
            print(f"{index}. {pr_details}")
            index += 1

if __name__ =='__main__':
    main()   


    