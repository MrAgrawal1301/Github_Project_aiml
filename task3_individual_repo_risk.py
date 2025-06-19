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

def select_particular_repo():
    index = 0
    print('Repositaries of Authenticated User are:')
    repos_inlist = list(user.get_repos())
    for index , repo in enumerate(repos):
        print(f'{index}. {repo.name}')
        index +=1

    askuser = int(input('Enter index No. of Repo:')) 
    if askuser > len(repos_inlist):
        return 'Enter valid no.'
    else:
        return askuser


def main():
    select_repo = select_particular_repo()
    try:
        stale_threshold_hours = int(input("Enter the number of hours to define a stale branch: "))
    except ValueError:
        return ("Invalid input. Please enter a valid number.")
    index = 1  
    selected_repo = list(repos)[select_repo]
    selected_repo_name = selected_repo.name 
    branches = selected_repo.get_branches()
    found_stale_branch = False
    for branch in branches:
        if branch.name != 'main':    
            branch_name = branch.name
            commit = selected_repo.get_commit(sha=branch.commit.sha)
            commit_date = commit.commit.committer.date 
            difference = cheak_time_delta(commit_date)
            if difference > timedelta(hours=stale_threshold_hours):
                found_stale_branch = True
                stale_branch_url = f"https://github.com/{user.login}/{selected_repo_name}/tree/{branch_name}"
                difference_days = difference.days
                risk_score = get_risk_score(difference_days)
                commit_author = commit.author
                author_name = commit_author.login if commit_author else "Unknown"
                print(f'{index}. [Repo Name: {selected_repo_name},\n Stale Branch url: {stale_branch_url},\n Author Name of Branch: {author_name},\n Last commit is ({difference}) old],\n Risk Level: {risk_score}]')
                index += 1
                print("Stale branch can me deleted")
    if not found_stale_branch:
        print('No Stale branch')

if __name__ == '__main__':
    main()