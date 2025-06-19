from task2_individual_repo import delete_branches , grouped_list
print(grouped_list , sep="\n")
if len(delete_branches)==0:
    print("no stale branch")
else:
    print("stale branch deleted")    


    