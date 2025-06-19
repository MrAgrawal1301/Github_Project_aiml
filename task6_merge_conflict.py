from github import Github 
from github import Auth
from datetime import timezone , datetime , timedelta
import json
import  os

def main():
    auth  = Auth.Token('')
    g = Github(auth = auth)
    user = g.get_user()
    repos = user.get_repos()
    index = 1
    print('Detail of all the merge conflict ---->')
    for repo in repos:
        prs = repo.get_pulls()
        counts_conflict = []
        for pr in prs:
            mergable_pr = pr.mergeable
            # if mergable_pr == False:
            counts_conflict.append(mergable_pr)
            merge_conflict_detail = {
                'prstatus': pr.mergeable_state , 
                'Repo Name': repo.name ,
                'Branch Name': pr.head.ref ,
                'pr_creator': pr.user.login
            }
            print(f'{index}. {json.dumps(merge_conflict_detail, indent=4)}')
            index += 1

if __name__ == '__main__':
    main()

