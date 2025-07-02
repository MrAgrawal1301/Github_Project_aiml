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
    for key, level in enumerate(range):
        if percentage <= range[level]:
            print(f"You are at Maturity Level {key}")
            print(f"\nTo improve your maturity level from {key} to {key + 1}, you should focus on the following rules:\n")
            return key
    print("You are already at the highest Maturity Level 5.")
    return 5

def give_rules_to_uplevel(data , range , pass_score , total_score , current_level):
    add_to_pass = []
    for i in data:
        if i['status'] == 'Fail':
            fail_score = float(i['score'])
            fail_weight = float(i['weight'])
            individual_fail_score = fail_score * fail_weight
            add_to_pass.append((i['ruleID'], i['rule_title'], i['severity'] , individual_fail_score))
    add_to_pass_scores_critical = []
    add_to_pass_scores_high = []
    add_to_pass_scores_medium = []
    add_to_pass_scores_low = []

    for i in add_to_pass:
        if i[2] == "Critical":
            add_to_pass_scores_critical.append(i)
        elif i[2] == "High":
            add_to_pass_scores_high.append(i)
        elif i[2] == "Medium":
            add_to_pass_scores_medium.append(i)
        elif i[2] == "Low":
            add_to_pass_scores_low.append(i)

    sorted_add_to_pass_scores_critical = sorted(add_to_pass_scores_critical, key=lambda x: x[3], reverse=True)
    sorted_add_to_pass_scores_high = sorted(add_to_pass_scores_high, key=lambda x: x[3], reverse=True)
    sorted_add_to_pass_scores_medium = sorted(add_to_pass_scores_medium, key=lambda x: x[3], reverse=True)
    sorted_add_to_pass_scores_low = sorted(add_to_pass_scores_low, key=lambda x: x[3], reverse=True)

    level_keys = list(range.keys())
    if current_level + 1 >= len(level_keys):
        print("You are already at the highest Maturity Level.")
        return
    next_level_index = current_level
    next_level = range[level_keys[next_level_index]]
    
    add_score = pass_score
    rules_to_add = []
    severity_list = [
        sorted_add_to_pass_scores_critical,
        sorted_add_to_pass_scores_high,
        sorted_add_to_pass_scores_medium,       
        sorted_add_to_pass_scores_low
    ]

    level_reached = False
    for severity_group in severity_list:
        for rule in severity_group:
            add_score = add_score + rule[3]
            new_percentage = (add_score / total_score) * 100
            rules_to_add.append(rule)
            print(f"New Percentage: {new_percentage:.2f}")
            if new_percentage >= next_level:
                level_reached = True
                break
        if level_reached:
            break    
    for rule in rules_to_add:
        print(f"Rule ID: {rule[0]}, Title: {rule[1]}, Severity: {rule[2]}")

def main():
    with open ('maturity.json' , 'r') as file:
        data = json.loads(file.read())
        total_score = calculate_total_score(data)
        pass_score = calculate_score_pass(data)
        percentage = (pass_score / total_score) * 100 if total_score > 0 else 0
        print(f'Maturity Score: {percentage:.2f}')
        range = {
            'Level 1': 20,
            'Level 2': 40,
            'Level 3': 60,
            'Level 4': 80,
            'Level 5': 100
        }
        current_level = maturity_level(percentage , range)
        give_rules_to_uplevel(data , range , pass_score , total_score , current_level)

if __name__ == "__main__":
    main()