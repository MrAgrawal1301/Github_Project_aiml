import json

def calculate_total_score(data):
    scores = []
    for i in data:
        score = float(i['score'])
        weight = float(i['weight'])
        individual_score = score * weight
        scores.append(individual_score)   
    sum_scores = sum(scores)
    return sum_scores
    
def calculate_score_pass(data):
    pass_scores = []
    for i in data:
        if i['status'] == 'Pass':
            pass_score = float(i['score'])
            pass_weight = float(i['weight'])
            individual_pass_score = pass_score * pass_weight
            pass_scores.append(individual_pass_score)
    sum_pass_scores = sum(pass_scores)
    return sum_pass_scores
    
def maturity_level(percentage, range):
    level_keys = list(range.keys())
    for level, score_sep in range.items():
        if percentage <= score_sep:
            return level
    return level_keys[-1]  

def give_rules_at_top_level(data , current_level):
    print("You are at good level but still you can improve your score.\nYou can work on the following rules to improve your score:")
    add_to_pass = []
    for i in data:
        if i['status'] == 'Fail':
            fail_score = float(i['score'])
            fail_weight = float(i['weight'])
            individual_fail_score = fail_score * fail_weight
            add_to_pass.append((i['ruleID'], i['rule_title'], i['resource'], i['severity'], individual_fail_score))
    sorted_add_to_pass = sorted(add_to_pass, key=lambda x: x[3], reverse=True)
    return sorted_add_to_pass

def give_rules_to_uplevel(data , range , pass_score , total_score , current_level):
    add_to_pass = []
    for i in data:
        if i['status'] == 'Fail':
            fail_score = float(i['score'])
            fail_weight = float(i['weight'])
            individual_fail_score = fail_score * fail_weight
            add_to_pass.append((i['ruleID'], i['rule_title'], i['resource'], i['severity'], individual_fail_score))
    add_to_pass_scores_critical = []
    add_to_pass_scores_high = []
    add_to_pass_scores_medium = []
    add_to_pass_scores_low = []
    for i in add_to_pass:
        if i[3] == "Critical":
            add_to_pass_scores_critical.append(i)
        elif i[3] == "High":
            add_to_pass_scores_high.append(i)
        elif i[3] == "Medium":
            add_to_pass_scores_medium.append(i)
        elif i[3] == "Low":
            add_to_pass_scores_low.append(i)

    sorted_add_to_pass_scores_critical = sorted(add_to_pass_scores_critical, key=lambda x: x[4], reverse=True)
    sorted_add_to_pass_scores_high = sorted(add_to_pass_scores_high, key=lambda x: x[4], reverse=True)
    sorted_add_to_pass_scores_medium = sorted(add_to_pass_scores_medium, key=lambda x: x[4], reverse=True)
    sorted_add_to_pass_scores_low = sorted(add_to_pass_scores_low, key=lambda x: x[4], reverse=True)

    level_keys = list(range.keys())
    next_level_index = int(int(current_level)-1)
    next_level = range[level_keys[next_level_index]]
    print(f"Next level score is {next_level}")
    add_score = pass_score
    severity_list = [
        sorted_add_to_pass_scores_critical,
        sorted_add_to_pass_scores_high,
        sorted_add_to_pass_scores_medium,       
        sorted_add_to_pass_scores_low
    ]
    rules_to_add = []
    level_reached = False
    for severity_group in severity_list:
        for rule in severity_group:
            add_score = add_score + rule[4]
            new_percentage = (add_score / total_score) * 100
            new_percentage = round(new_percentage, 2)
            rules_to_add.append(rule)
            if new_percentage > next_level:
                level_reached = True
                break
        if level_reached == True:
            break
    return rules_to_add , new_percentage

with open ('maturity.json' , 'r') as file:
    data = json.loads(file.read())
    total_score = calculate_total_score(data)
    pass_score = calculate_score_pass(data)
    percentage = (pass_score / total_score) * 100 if total_score > 0 else 0
    percentage = round(percentage, 2)
    if percentage == 0.0:
        print("\nUnfortunately no rule passed , You should work on the rules to improve your score.\n")
    print(f'Maturity Score: {percentage}')
    range = {
        '1': 20,   # Maturity Level 1: between 0 to 20 including 20
        '2': 40,   # Maturity Level 2: between 20 to 40 including 40
        '3': 60,   # Maturity Level 3: between 40 to 60 including 60
        '4': 92,   # Maturity Level 4: between 60 to 80 including 80
        '5': 100   # Maturity Level 5: between 80 to 100 including 100
    }
    current_level = maturity_level(percentage , range)
    print(f'Current Maturity is Level {current_level}')
    if current_level == '5':
        print("You are already at the Highest Maturity Level.")
        improvement_rules = give_rules_at_top_level(data , current_level)
        for index , rule in enumerate(improvement_rules):
            print(f"""{index +1}: Rule ID: {rule[0]}, Title: {rule[1]},Resource: {rule[2]}, Severity: {rule[3]}\n""")
    else:
        print(f"To reach from level {current_level} to level {int(current_level) + 1}, you need to pass the following rules:")
        uplevel_rule , new_percentage = give_rules_to_uplevel(data , range , pass_score , total_score , current_level)
        for index , rule in enumerate(uplevel_rule):
            print(f"""{index +1}: Rule ID: {rule[0]}, Title: {rule[1]},Resource: {rule[2]}, Severity: {rule[3]}\n""")
        print(f"New score: {new_percentage}")
