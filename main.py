# List in pos 0 is for SAD classes, list in pos 1 is for 2AD classes, list in pos 2 is for 3AD classes
list_class_by_ability_depend = [
    ["Bard", "Cleric (Caster)", "Druid", "Fighter (Ranged)", "Rogue (Ranged)", "Sorcerer", "Warlock (Ranged)",
     "Wizard"], ["Barbarian", "Fighter (Melee)", "Ranger", "Rogue (Melee)", "Warlock (Hexblade)"],
    ["Cleric (Melee)", "Monk", "Paladin"]]
# Barbarian is recommended when Strength and Constitution are both in the top 3 scores
bound_barbarian = ["Barbarian", [3, 6, 3, 6, 6, 6]]
# Bard is recommended when Charisma is the best stat
bound_bard = ["Bard", [6, 6, 6, 6, 6, 1]]
# Caster Clerics can be recommended if Wisdom is best stat. Melee Clerics can be recommended if Strength,
# Constitution and Wisdom are in top 4 scores
bound_cleric_caster = ["Cleric (Caster)", [6, 6, 6, 6, 1, 6]]
bound_cleric_melee = ["Cleric (Melee)", [4, 6, 4, 6, 4, 6]]
# Druid is recommended when Wisdom is the best stat
bound_druid = ["Druid", [6, 6, 6, 6, 1, 6]]
# Fighter can be recommended if Strength or Dexterity are in top 2 scores and Constitution is  in top 4 scores
bound_fighter_str = ["Fighter (Strength)", [2, 6, 4, 6, 6, 6]]
bound_fighter_dex = ["Fighter (Dexterity)", [6, 2, 4, 6, 6, 6]]
# Monk is recommended if Dex is in top 2 scores, and Constitution and Wisdom are in top 4 scores
bound_monk = ["Monk", [6, 2, 4, 6, 4, 6]]
# Paladin can be recommended if (Strength or Dexterity), Constitution and Charisma are in top 4 scores
bound_paladin_str = ["Paladin (Strength)", [4, 6, 4, 6, 6, 4]]
bound_paladin_dex = ["Paladin (Dexterity)", [6, 4, 4, 6, 6, 4]]
# Ranger is recommended when Dexterity is the top 2 stats, and either Wisdom or Constitution are in top 3 stats
bound_ranger_con = ["Ranger (Martial-Leaning)", [6, 2, 3, 6, 6, 6]]
bound_ranger_wis = ["Ranger (Caster-Leaning)", [6, 2, 6, 6, 3, 6]]
# Rogue is recommended when Dexterity is the best stat
bound_rogue = ["Rogue", [6, 1, 6, 6, 6, 6]]
# Sorcerer is recommended when Charisma is the best stat
bound_sorcerer = ["Sorcerer", [6, 6, 6, 6, 6, 1]]
# Warlock is recommended when Charisma is the best stat
bound_warlock = ["Warlock", [6, 6, 6, 6, 6, 1]]
# Wizard is recommended when Intelligence is the best stat
bound_wizard = ["Wizard", [6, 6, 6, 1, 6, 6]]


def unbound_array_recommend(stats):
    trans_stats = unbound_array_transform(stats)
    eval_result = unbound_array_eval(trans_stats)
    select_print_list(eval_result, 2, "Highly recommended:", list_class_by_ability_depend)
    select_print_list(eval_result, 1, "Recommended:", list_class_by_ability_depend)
    select_print_list(eval_result, 0, "Not recommended:", list_class_by_ability_depend)


# For stat arrays which are not bound yet, we want to rewrite the stat array as decreases from top stat
def unbound_array_transform(array):
    array.sort(reverse=True)
    peak = array[0]
    new_array = []
    for i in array:
        new_array.append(i - peak)
    return new_array


# SAD classes are always a decent choice, highly recommended if drop from 1st to 2nd is 3 or more.
# 2 stat classes playable if drop from 1st to 2nd in second stat is 2 or less,
# highly recommended if drop from 1st to 2nd is 0 or 1 and drop from 2nd to 3rd is 2 or more.
# 3 stat classes playable if drop from 1st to 3rd in second stat is 2 or less,
# highly recommended if drop from 1st to 3rd is 0 or 1.
# In returned array, 0 = not recommended, 1 = playable, 2 = highly recommended
def unbound_array_eval(array):
    class_rec = [0, 0, 0]
    if (array[0]) > (array[1] + 2):
        class_rec[0] += 2
        return class_rec
    class_rec[0] += 1
    if ((array[0]) <= (array[1] + 1)) and ((array[1]) > (array[2] + 1)):
        class_rec[1] += 2
        return class_rec
    class_rec[1] += 1
    if (array[0]) <= (array[2] + 2):
        class_rec[2] += 1
    if (array[0]) <= (array[2] + 1):
        class_rec[2] += 1
    return class_rec


def print_list(p_list):
    for i in p_list:
        print(" " + i)


# eval_list and p_list MUST be the same length
def select_print_list(eval_list, target, pretext, p_list_list):
    print(pretext)
    n = -1
    for i in eval_list:
        n += 1
        if i == target:
            print_list(p_list_list[n])


# Remember order of bound stats are STR, DEX, CON, INT, WIS, CHA
def bound_array_recommend(stats):
    trans_stats = bound_array_transform(stats)
    print("Recommended:")
    check_bound(trans_stats, bound_barbarian)
    check_bound(trans_stats, bound_bard)
    check_bound(trans_stats, bound_cleric_caster)
    check_bound(trans_stats, bound_cleric_melee)
    check_bound(trans_stats, bound_druid)
    check_bound(trans_stats, bound_fighter_str)
    check_bound(trans_stats, bound_fighter_dex)
    check_bound(trans_stats, bound_monk)
    check_bound(trans_stats, bound_paladin_str)
    check_bound(trans_stats, bound_paladin_dex)
    check_bound(trans_stats, bound_ranger_con)
    check_bound(trans_stats, bound_ranger_wis)
    check_bound(trans_stats, bound_rogue)
    check_bound(trans_stats, bound_sorcerer)
    check_bound(trans_stats, bound_warlock)
    check_bound(trans_stats, bound_wizard)


# To actually get the correct ordering of the stats we get how many scores an ability score is greater than or equal to
# (including self), then subtract this number from 7. This is to handle ties correctly.
def bound_array_transform(array):
    trans_array = []
    for i in range(6):
        check_threshold = array[i]
        pass_count = 0
        for n in range(6):
            if check_threshold >= array[n]:
                pass_count += 1
        trans_array.append(7 - pass_count)
    return trans_array


def check_bound(bound_stats, check_list):
    if eval_bound(bound_stats, check_list[1]):
        print(" " + check_list[0])


# Each class has certain ability scores that should be prioritised to different degrees
# To recommend a class, the needed class attributes
def eval_bound(bound_stats, eval_list):
    for i in range(6):
        if bound_stats[i] > eval_list[i]:
            return False
    return True


def main():
    while True:
        array_type = input("Type U(u) for unbound stat array, B(b) for bound stat array, Q(q) to quit").upper()
        if array_type == "U":
            unbound_array_function()
        elif array_type == "B":
            bound_array_function()
        elif array_type == "Q":
            quit()
        else:
            print("Invalid input, please try again")


def unbound_array_function():
    input_array = take_array(False)
    unbound_array_recommend(input_array)


def bound_array_function():
    input_array = take_array(True)
    bound_array_recommend(input_array)


def take_array(bound):
    while True:
        if bound:
            raw_input = input("Type in your rolls in the format: STR DEX CON INT WIS CHA ")
        else:
            raw_input = input("Type in your rolls in the format: Roll1 Roll2 Roll3 Roll4 Roll5 Roll6 ")
        split_input = raw_input.split(" ")
        try:
            processed_input = process_split_input(split_input)
            return processed_input
        except:
            print("Incorrect input, please use correct formatting")


def process_split_input(split_input):
    if len(split_input) != 6:
        raise ValueError
    output = []
    for i in split_input:
        output.append(int(i))
    return output




if __name__ == "__main__":
    main()