# Github_Project_aiml


REPORT
GitHub Stale Branches 
Purpose:
The script connects to the GitHub API using a personal access token (classic) to identify branches across all repositories of an authenticated user that have not had any commits for a specified number of hours. It lists branches considered "stale" based on user input and collects information about them, potentially to be deleted.

Key Functionalities:
1.	Authentication:
    o	Uses the PyGithub library to get access of GitHub via a personal access token loaded from an environment variable (GITHUB_TOKEN).
2.	User Input:
    o	Takes an integer input from the user to specify the no. of hours to identifying stale branches.
3.	Time Calculation:
    o	Defines a function checktimedelta(timestamp) which calculates the time difference between the current UTC time and the timestamp of the last commit on a branch.
4.	Branch Inspection:
    o	Inspect all the repositories of the authenticated user.
    o	For each repository, identifies through all branches.
    o	Gets the commit date of the latest commit on each branch.
    o	Calculates the time difference since the last commit.
    o	If this time difference exceeds the user-specified time (in hours), the branch is marked as stale.
5.	Data Collection:
    o	Collects information about stale branches including:
        -	Repository name
        -	Branch name
        -	Date of the last commit
        -	Difference in time 
    o	Also collects URLs of branches identified for potential deletion.
6.	Output:
    o	Prints the GitHub username (user.login). To check its u as user only.
    o	Stores the stale branches’ info and URLs for further use (e.g., review, deletion).


Summary:
This script is a good starting point for managing GitHub branches by identifying stale branches based on the time since their last commit. Further improvements can extend it to safely delete stale branches and handle errors gracefully.


this is the great project of mridul agrawal


 
