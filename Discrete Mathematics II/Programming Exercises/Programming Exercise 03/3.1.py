from pyscipopt import Model, quicksum, multidict
import csv
import os

def file_paths():
    """
    setting the file paths
    """
    script_dir = os.path.dirname(__file__)

    # setting the file path for allfoods.csv
    allfoods_rel_path = "data/allfoods.csv"
    allfoods_abs_file_path = os.path.join(script_dir, allfoods_rel_path)

    # setting the file path for reference.csv
    reference_rel_path = "data/reference.csv"
    reference_abs_file_path = os.path.join(script_dir, reference_rel_path)

    return allfoods_abs_file_path, reference_abs_file_path

def import_csv(allfoods_abs_file_path, reference_abs_file_path):
    with open(allfoods_abs_file_path, newline='') as csvfile:
            allfoods = csv.DictReader(csvfile, delimiter=';')
            
    with open(reference_abs_file_path, newline='') as csvfile:
            reference = csv.DictReader(csvfile, delimiter=';')

    return allfoods, reference

if __name__ == "__main__":
    allfoods_abs_file_path, reference_abs_file_path = file_paths()
    allfoods, reference = import_csv(allfoods_abs_file_path, reference_abs_file_path)
    