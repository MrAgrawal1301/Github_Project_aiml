from github import Github 
from datetime import timezone , datetime , timedelta
import json
from github import Auth

#when we use the auth then we can only get access to private repo and with .env no access to private repo......

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
            return f"{a} --> The Stale branch is {stale_time} days old"
    return f"Critical Risk --> The Stale branch is {stale_time} days old"   

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
            return f'{a} --> The PR is created {created_day} days ago.'
    return f'Critical Risk --> The PR is created {created_day} days ago.'
    
def contributor_data(repos):
    index = 1
    for repo in repos:
        contributes = repo.get_contributors()
        branches = repo.get_branches()                
        for branch in branches:
            for contributer in contributes:
                contributer_details = {
                    'Contributor Name': contributer.login,
                    'Repo Name': repo.name,
                    'Branch Name': branch.name,
                    'No. of Commits': contributer.contributions
                }
                print(f'{index}. Contributions: {json.dumps(contributer_details,indent=4)}')
                index += 1

def stale_branches(repos , stale_threshold_hours , user):
    
    repo_name_list = []  
    for repo in repos:
        repo_name = repo.name
        repo_name_list.append(repo.name)
        index=0
        while index < len(repo_name_list):
            print(f"{index}. {repo_name_list[index]}")
            index +=1
    for repo in repos:
        index = 1
        found_stale_branch = False
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
                stale_detail = {
                    'Repo Name': repo_name, 
                    'Stale Branch url': stale_branch_url,
                    'Author Name of Branch': author_name, 
                    'Last commit is DateTime': str(difference) ,
                    'Risk Level': risk_score
                    }
                print(f'{index}. {json.dumps(stale_detail, indent=4)}')
                index += 1
    if not found_stale_branch:
        print("No Stale Branch")            
                              
def pullrequests(repos):
    found_pr = False
    index = 1
    for repo in repos:
        repo_name = repo.name
        prs = repo.get_pulls(state='all')
        for pr in prs:
            filebook = []
            get_oneday = {}
            found_pr = True
            created_time = pr.created_at
            time_difference_from_created_date = cheak_time_delta(created_time)
            difference_createdat_in_days = time_difference_from_created_date.days
            risk_level = get_risk_score_pr(difference_createdat_in_days)
            commits = pr.get_commits()  
            for commit in commits:
                dateis = commit.commit.committer.date
                if dateis.tzinfo is None:
                    timestamp = dateis.replace(tzinfo = timezone.utc)
                dateis = dateis.date()
                if dateis in get_oneday:
                    get_oneday[dateis] += 1
                else:
                    get_oneday[dateis] = 1
            frequancy = None            
            for a,b in get_oneday.items():
                if b > 2:
                    frequancy = 'Not a good PR'
                    break
            else:
                frequancy = 'Can be a good PR'    
            files =pr.get_files()
            for file in files:
                filebook.append(file.filename)           
            pr_details ={
                'Repo Name': repo_name,
                'PullRequest': pr.title,
                'No. of Commits': pr.commits,
                'Author': pr.user.login,
                'frequancy': frequancy,
                'State': pr.state, 
                'Created at': str(pr.created_at) if pr.created_at else None,
                'Seen at': str(pr.closed_at) if pr.closed_at else None,
                'Risk level': risk_level,
                'Merge Date': str(pr.merged_at) if pr.merged_at else None,
                'Merged by': pr.merged_by.login if pr.merged_by else None,
                'When the pr was again updated': str(pr.updated_at) if pr.updated_at else None,
                'Files in which changes were done': filebook
                }
            print(f'{index}. {json.dumps(pr_details, indent=4)}')
            index += 1
    if not found_pr:
        print('No Pull Requests')
                        
def main():
    get_pat = input("Enter Your PAT:")
    print('-----------------------------------------------------------------Starting Analyis-----------------------------------------------------------------')
    auth = Auth.Token(get_pat)
    g = Github(auth = auth)
    user = g.get_user()
    print(user.login)
    repos = user.get_repos()
    print(f'\nDetail of Contributors for {user.login} -->\n')
    data_contribution = contributor_data(repos)
    print(f'\nDetals of stale branches for {user.login} -->\n')
    stale_threshold_hours_dict = {
        'time in hour': 1
    } 
    for a , b in stale_threshold_hours_dict.items():
        stale_threshold_hours_entry = b     
    data_stale_branch = stale_branches(repos , stale_threshold_hours_entry , user)  
    print(f'\nDetals of pull requests for {user.login} -->\n')
    data_pull_request = pullrequests(repos)

if __name__ =='__main__':
    main()
