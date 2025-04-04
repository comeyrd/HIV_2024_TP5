import random
import string
def mutate_tests(tests,best_test):
    if isinstance(tests[0][0]["in"],int):
        mutate_input =  mutate_input_int
    elif isinstance(tests[0][0]["in"],str):
        mutate_input = mutate_input_str
    else : 
        raise KeyError("error str int")

    for j in range(len(tests)):
        suite = tests[j][:]
        num_mutations = random.randint(1, max(1, len(suite) // 2))
        tests_to_mutate = random.sample(suite, num_mutations)
        for i in range(len(suite)):
            if suite[i] in tests_to_mutate:
                suite[i]["in"] = mutate_input(suite,i)
        tests.append(suite)
    for m in range(6):
        n_suite = best_test[:]
        num_mutations = random.randint(1, max(1, len(suite) // 2))
        tests_to_mutate = random.sample(suite, num_mutations)
        for n in range(len(suite)):
            n_suite.append({"in":mutate_input(suite,i),"out":""})
        tests.append(n_suite)
    return tests


def mutate_input_int(suite,i):
    mutations = [_int_add_random_item,_int_divide_random_item,_int_subtract_random_item,_int_zero]
    return random.choice(mutations)(suite,i)

def _int_add_random_item(suite,i):
    to_add = random.choice(suite)
    temp = suite[i]["in"] + to_add["in"]
    return temp 

def _int_divide_random_item(suite, i):
    to_divide = random.choice(suite)
    if to_divide["in"] == 0:  
        to_divide["in"] = 1
    temp = suite[i]["in"]// to_divide["in"]
    return temp 

def _int_subtract_random_item(suite, i):
    to_subtract = random.choice(suite)
    temp = suite[i]["in"]- to_subtract["in"]
    return temp 

def _int_zero(suite, i):
    return 0 
import random

def _str_reverse(suite, i):
    temp = suite[i]["in"][::-1]
    return temp 

def _str_shuffle(suite, i):
    shuffled = list(suite[i]["in"])
    random.shuffle(shuffled)
    temp = "".join(shuffled)
    return temp 

def _str_duplicate_random_char(suite, i):
    pos = random.randint(0, len(suite[i]["in"]) - 1)
    temp = suite[i]["in"][:pos] + suite[i]["in"][pos] + suite[i]["in"][pos:]
    return temp 

def _str_remove_random_char(suite, i):
    pos = random.randint(0, len(suite[i]["in"]) - 1)
    temp = suite[i]["in"][:pos] + suite[i]["in"][pos+1:]
    return temp 

def _str_toggle_case(suite, i):
    temp = suite[i]["in"].swapcase()
    return temp 

def _str_add_random_char(suite, i):
    if suite[i]["in"]:
        pos = random.randint(0, len(suite[i]["in"]) - 1)  # Choose a random position
        random_char = random.choice(string.ascii_letters + string.digits)  # Choose a random character
        # Insert the random character at the selected position
        temp = suite[i]["in"][:pos] + random_char + suite[i]["in"][pos:]
        return temp
    

def mutate_input_str(suite, i):
    mutations = [_str_reverse,_str_shuffle,_str_add_random_char,_str_duplicate_random_char,_str_remove_random_char,_str_toggle_case]
    return random.choice(mutations)(suite, i)

