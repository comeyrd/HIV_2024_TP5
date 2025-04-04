from get_coverage import run_coverage_with_inputs
import google.generativeai as genai
import json
import random
from _mutation import mutate_tests

code_dir = "./to_test/"
test_dir = "./tests/test_"

model = None

def header_prompt(fn):
    prompt = f"""Generate inputs and asserted outputs for the function {fn}
Try to achieve 100 percent coverage
Write back only a json array within each object the input in 'in' and your predicted output in 'out' """ 
    return prompt

def get_file_content(filename):
    with open(code_dir + filename+".py", "r") as file:
        return file.read()

def clean_and_fix_indentation(code):
    lines = code.strip().split("\n")

    if lines[0].startswith("```"):
        lines.pop(0)
    if lines[-1].startswith("```"):
        lines.pop(-1)

    cleaned_code = "\n".join(lines)
    return cleaned_code

def write_generated_test(fun,test):
    test = clean_and_fix_indentation(test)
    with open(f"{test_dir}{fun}.py", "w") as file:
        file.write(test)
    return f"{test_dir}{fun}"

def generate_full_prompt(fun):
    prompt = header_prompt(fun)
    code = get_file_content(fun)
    prompt = prompt+ "\n [FUNCTION]\n "+code+ "\n [FUNCTION]\n " 
    return prompt

def setup_gemini():
    key = "AIzaSyB_JowL8AkPUUL_wOWlvUEb3xbUW9Ma0HA"
    genai.configure(api_key=key)
    global model
    model = genai.GenerativeModel('models/gemini-2.0-flash')

def random_subsets(test_suite,L_set,N_cases=10):
    subsets = []
    if(N_cases > len(test_suite)):
        return generate_reduced_subsets(test_suite)
    for _ in range(N_cases):
        subset_size = random.randint(1, len(test_suite)-1)  # Random size
        subset = random.sample(test_suite, subset_size)  # Randomly select tests
        subsets.append(subset)
    return subsets
    

def generate_reduced_subsets(test_suite):
    subsets = [test_suite[:i] + test_suite[i+1:] for i in range(len(test_suite))]
    return subsets

def ask_gemini(prompt):
    return model.generate_content(prompt).text

def reduce_base_test(test):
    return random.sample(test,len(test)//4)

def Test_with_llm(evaluations,to_test):
    setup_gemini()
    for test_function in to_test:
        print(f"Testing {test_function}")
        print("Querying the LLM …")
        prompt = generate_full_prompt(test_function)
        generated_test = json.loads(clean_and_fix_indentation(ask_gemini(prompt)))
        coverage_llm = run_coverage_with_inputs(generated_test,test_function)
        print("Iterating without mutation of input")
        iterate(test_function,evaluations,generated_test,coverage_llm)
        print("Iterating with mutation of input")
        iterate(test_function,evaluations,generated_test,coverage_llm,True)

        print("Testing with a reduced base test from the LLM")
        generated_test = reduce_base_test(generated_test)
        coverage_llm = run_coverage_with_inputs(generated_test,test_function)
        print("Iterating without mutation of input")
        iterate(test_function,evaluations,generated_test,coverage_llm)
        print("Iterating with mutation of input")
        iterate(test_function,evaluations,generated_test,coverage_llm,True)




def iterate(test_function,evaluations,generated_test,coverage_llm,mutate=False):
        best_coverage = coverage_llm[test_function+".py"]
        best_test = generated_test
        print(f'LLM results, line : {best_coverage["line_rate"]} | branch : {best_coverage["branch_rate"]} | n_test {best_coverage["n_test"]}\n')
        for i in range(evaluations):
            better = False
            ## Reduce the number of tests tests
            tests = random_subsets(best_test,len(best_test))
            if mutate:
                tests = mutate_tests(tests,best_test)
            for test_case in tests:
                coverage = run_coverage_with_inputs(test_case,test_function)[test_function+".py"]
                is_better_coverage = (
                    coverage["line_rate"] > best_coverage["line_rate"] or
                    coverage["branch_rate"] > best_coverage["branch_rate"])
                is_same_coverage_but_fewer_tests = (
                    coverage["line_rate"] >= best_coverage["line_rate"] and
                    coverage["branch_rate"] >= best_coverage["branch_rate"] and
                    coverage["n_test"] < best_coverage["n_test"])
                
                if is_better_coverage or is_same_coverage_but_fewer_tests:
                    best_test = test_case
                    best_coverage = coverage
                    #print(f'    New best test suite, line : {best_coverage["line_rate"]} | branch : {best_coverage["branch_rate"]} | n_test {best_coverage["n_test"]}')
                    better = True
            if better : 
                print("+",end="",flush=True)
            else:
                print(".",end="",flush=True)
        print(f'\n Best test suite for {test_function} line : {best_coverage["line_rate"]} | branch : {best_coverage["branch_rate"]} | n_test {best_coverage["n_test"]}')
        print(best_test)
        print("------")
        

if __name__ == "__main__":
    evaluations = 100
    to_test = ["number_to_words","strong_password_checker"]
    Test_with_llm(evaluations,to_test)
    
