import os 
from github import Github 
from datetime import timezone , datetime , timedelta
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

def cheak_time_delta(timestamp):
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo = timezone.utc)
    now = datetime.now(timezone.utc)
    difference = now - timestamp
    return difference

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

def contributor_data(repos):
    for repo in repos:
        contributes = repo.get_contributors()
        branches = repo.get_branches()
        prs = repo.get_pulls()
        for pr in prs:
            print(f'Contributor: {pr.user.login} has PR {pr.state} in Repository {repo.name} from contributer branch ({pr.head.ref}) to my {repo.name} branch ({pr.base.ref})')
        for branch in branches:
            for contributer in contributes:
                print(f'Contributor: {contributer.login} made {contributer.contributions} commits to repository {repo.name} in branch ({branch.name})')

def stale_branches(repos , stale_threshold_hours , user):
    index = 1
    found_stale_branch = False  
    for repo in repos:
        repo_name = repo.name 
        branches = repo.get_branches()
        for branch in branches:    
            branch_name = branch.name
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
                print(f'{index}. [Repo Name: {repo_name},\n Stale Branch url: {stale_branch_url},\n Author Name of Branch: {author_name},\n Last commit is ({difference}) old],\n Risk Level: {risk_score}]')
                index += 1
    if not found_stale_branch:
        print('No Stale Branch')  
                              
def pullrequests(repos):
    index = 1
    found_pr = False
    for repo in repos:
        repo_name = repo.name
        prs = repo.get_pulls(state='all')
        filebook = []    
        for pr in prs:
            found_pr = True
            created_time = pr.created_at
            time_difference_from_created_date = cheak_time_delta(created_time)
            difference_createdat_in_days = time_difference_from_created_date.days
            risk_level = get_risk_score_pr(difference_createdat_in_days)
            files =pr.get_files()
            for file in files:
                filebook.append(file.filename)            
            pr_details = f"[Repo Name: {repo_name} | PullRequest: {pr.title} | Author: {pr.user.login} | State: {pr.state} | Created at: {pr.created_at} | Seen at: {pr.closed_at} |Risk level: {risk_level} | Merge Date: {pr.merged_at} | Merged by: {pr.merged_by} | When the pr was again updated: {pr.updated_at} | Files in which changes were done: {filebook}]"
            print(f"{index}. {pr_details}")
            index += 1
    if not found_pr:
        print('No Pull Requests')
                        
def main():
    username = input('Enter user name:')
    user = g.get_user(username)
    repos = user.get_repos()
    print(f'Detail of Contributors for {username} -->')
    data_contribution = contributor_data(repos)
    print(f'Detals of stale branches for {username} -->')
    try:
        stale_threshold_hours_entry = int(input("Enter the number of hours to define a stale branch: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")   
    data_stale_branch = stale_branches(repos , stale_threshold_hours_entry , user)  
    print(f'Detals of pull requests for {username} -->')
    data_pull_request = pullrequests(repos)

if __name__ =='__main__':
    main()