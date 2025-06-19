from jira import Comment ,  Issue , JIRA , JIRAError , Priority , Project , User , Role , Watchers , Worklog

from jira import JIRA
jira = JIRA(
    #options={'server':'http://19garwal.atlassian.net/'},
   # basic_auth=(#'1983l@gmail.com', '#ATATT3xFfGF0s2gEzNbV3oExDaQzy_E=8754A606')
)
users = jira.search_users(query='1983mridulagarwal@gmail.com')
for user in users:
    print(f"Display Name: {user.displayName}")
    print(f"Account ID: {user.accountId}")

projects = jira.projects()
for project in projects:
    print('----------------------------------START------------------------------------')
    print(project.id)
    print(project.key)
    print(project.name)
    print('-----------------------------------END-------------------------------------')
    issues = jira.search_issues(f'project = {project}')
    for issue in issues:
        print(f'{issue.key} | {issue.fields.project} | {issue.fields.status} | {issue.fields.summary}')
   












   
      