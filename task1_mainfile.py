from task1_find_stale_repo import delete_branches
print("Path of stale branches are:")
print(*delete_branches , sep="\n")
if len(delete_branches)==0:
    print("no stale branch")
else:
    print("stale branch deleted")    


    