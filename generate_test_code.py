from get_coverage import run_coverage_with_unittest
import google.generativeai as genai

code_dir = "./to_test/"
test_dir = "./tests/test_"

model = None

def load_key():
    with open("key.secret") as file:
        return file.read()

def header_prompt(fn):
    prompt = f"""Generate a unittest for the function {fn}
Try to achieve 100 percent coverage
Write back only the test code so it can be directly executed, dont forget the if main
import the function with "from to_test.{fn} import {fn}"
""" 
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
    key = load_key()
    genai.configure(api_key=key)
    global model
    model = genai.GenerativeModel('models/gemini-2.0-flash')

def ask_gemini(prompt):
    return model.generate_content(prompt).text

if __name__ == "__main__":
    to_test = ["number_to_words","strong_password_checker"]
    setup_gemini()
    for test in to_test:
        prompt = generate_full_prompt(test)
        generated_test = ask_gemini(prompt)
        test_dir = write_generated_test(test,generated_test)
    to_test_py = [x+".py" for x in to_test]
    result = run_coverage_with_unittest("tests",to_test_py)
    print(result)

