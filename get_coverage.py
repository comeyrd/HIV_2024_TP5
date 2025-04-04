import coverage
import unittest
import tempfile
import importlib


def run_coverage_with_unittest(test_dir,functions):
    # Start coverage with the --branch option
    cov = coverage.Coverage(branch=True)
    cov.start()

    loader = unittest.defaultTestLoader
    suite = loader.discover(test_dir)  # Replace with your test directory/module
    runner = unittest.TextTestRunner()
    runner.run(suite)

    # Stop coverage and save the results
    cov.stop()
    cov.save()
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        # Get the file path from the NamedTemporaryFile object
        tmpfile_path = tmpfile.name

    # Now, generate the coverage report in the temporary file path
    cov.xml_report(outfile=tmpfile_path)

    # Read the content of the temporary file
    with open(tmpfile_path, 'r') as file:
        xml_data = file.read()

    classes_info = get_classes_for_package(xml_data,functions)
    return classes_info


def run_coverage_with_inputs(inputs,fn_name):
     # Start coverage with the --branch option
    cov = coverage.Coverage(branch=True)
    cov.start()
    module = importlib.import_module("to_test."+fn_name)
    importlib.reload(module)
    fn = getattr(module, fn_name)
    # Stop coverage and save the results
    passing = 0
    failing = 0
    for item in inputs:
        try:
            result = fn(item["in"])
            if result == item["out"]:
                passing+=1
            else:
                failing+=1
                item["out"] = result
        except Exception as _:
            failing+=1
    result = {}
    result["passing"] = passing
    result["failing"] = failing
    result["tests"] = passing + failing
    cov.stop()
    cov.save()
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        # Get the file path from the NamedTemporaryFile object
        tmpfile_path = tmpfile.name

    # Now, generate the coverage report in the temporary file path
    cov.xml_report(outfile=tmpfile_path)

    # Read the content of the temporary file
    with open(tmpfile_path, 'r') as file:
        xml_data = file.read()
    #print(xml_data)
    classes_info = get_classes_for_package_s(xml_data,fn_name,result["tests"])

    return classes_info


import xml.etree.ElementTree as ET

def get_classes_for_package(xml_data,functions):
    # Parse the XML data
    root = ET.fromstring(xml_data)
    packages_element = root.find('packages')
    for package_elem in packages_element.findall("package"):
        classes_info = {}
        classes = package_elem.find('classes')
        for class_elem in classes.findall("class"):
            class_name = class_elem.get("name")
            if class_name in functions:
                line_rate = class_elem.get("line-rate")
                branch_rate = class_elem.get("branch-rate")
                classes_info[class_name] = { "line_rate": float(line_rate) if line_rate else None,"branch_rate": float(branch_rate) if branch_rate else None}
    return classes_info

def get_classes_for_package_s(xml_data,function,nb_test):
    # Parse the XML data
    root = ET.fromstring(xml_data)
    packages_element = root.find('packages')
    for package_elem in packages_element.findall("package"):
        classes_info = {}
        classes = package_elem.find('classes')
        for class_elem in classes.findall("class"):
            class_name = class_elem.get("name")
            if class_name == (function+".py"):
                line_rate = class_elem.get("line-rate")
                branch_rate = class_elem.get("branch-rate")
                classes_info[class_name] = { "line_rate": float(line_rate) if line_rate else None,"branch_rate": float(branch_rate) if branch_rate else None,"n_test":nb_test}
    return classes_info

def read_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content
