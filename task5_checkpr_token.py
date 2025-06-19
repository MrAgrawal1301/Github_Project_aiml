#Enter the github username:Rajeev-831

# No Open PR by  Rajeev-831

# Rajeev-831 has not created any branches in the authenticated user's repos.
#this code is to cheak whether the user we enter have any pr or branch in token user 

from github import Github
import os
from datetime import timedelta , timezone , datetime
from dotenv import load_dotenv
load_dotenv()

# Rajeev-831   Mridu1883
def cheak_time_delta(timestamp):
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo = timezone.utc)
    now = datetime.now(timezone.utc)
    difference = now - timestamp
    return difference

def get_risk_score_pr(created_day):
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

def get_risk_score_branches(stale_time):
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

def pullrequests(repo , pr ):
    print('\nPull Request detail:\n')
    index = 1
    found_pr = False
    repo_name = repo.name
    filebook = []    
    found_pr = True
    created_time = pr.created_at
    time_difference_from_created_date = cheak_time_delta(created_time)
    difference_createdat_in_days = time_difference_from_created_date.days
    risk_level = get_risk_score_pr(difference_createdat_in_days)
    files =pr.get_files()
    for file in files:
        filebook.append(file.filename)            
    pr_details = f"[Repo Name: {repo_name} | PullRequest: {pr.title} | Author: {pr.user.login} | State: {pr.state} | Created at: {pr.created_at} | Seen at: {pr.closed_at} |Risk level: {risk_level} | Merge Date: {pr.merged_at} | Merged by: {pr.merged_by} | When the pr was again updated: {pr.updated_at} | Files in which changes were done: {filebook}]"
    print(f"\n{index}. {pr_details}")
    index += 1
    if not found_pr:
        print('No Pull Requests')

def stale_branches(repo , branch , user): 
    print('\nStale Branch Detail:\n')
    stale_threshold_hours = stale_time = int(input("Enter No. of Hours:"))
    repo_name = repo.name
    branch_name = branch.name
    index = 1
    found_stale_branch = False  
    commit = repo.get_commit(sha=branch.commit.sha)
    commit_date = commit.commit.committer.date 
    difference = cheak_time_delta(commit_date)
    if difference > timedelta(hours=stale_threshold_hours):
        found_stale_branch = True
        stale_branch_url = f"https://github.com/{user.login}/{repo_name}/tree/{branch_name}"
        difference_days = difference.days
        risk_score = get_risk_score_branches(difference_days)
        commit_author = commit.author
        author_name = commit_author.login if commit_author else "Unknown"
        print(f'\n{index}. [Repo Name: {repo_name},\n    Stale Branch url: {stale_branch_url},\n    Author Name of Branch: {author_name},\n    Last commit is ({difference}) old],\n    Risk Level: {risk_score}]')
        index += 1   
    if not found_stale_branch:
        print('\nStale Branch Detail:\n')
        print('\nNo Stale Branch')  

def main():
    token = os.getenv('GITHUB_TOKEN')
    g = Github(token)
    username = input('Enter the github username:')
    other_user = g.get_user(username)
    user = g.get_user()
    repos = user.get_repos()
    has_pr = False
    for repo in repos:
        repo_name = repo.name
        prs = repo.get_pulls()
        for pr in prs:
            if pr.user.login == username:
                has_pr = True
                pullrequests(repo , pr)

    if not has_pr:
        print('\nNo Open PR by ' , username)


    has_branch = False 
    for repo in repos:
        branches = repo.get_branches()
        for branch in branches:
            branch_name = branch.name
            get_commits = branch.commit.commit.author
            if get_commits.name == username:
                has_branch = True
                stale_branch_user = stale_branches(repo , branch , user)

    if not has_branch:
        print(f"\n{username} has not created any branches in the authenticated user's repos.")


if __name__ == '__main__':
    main()
