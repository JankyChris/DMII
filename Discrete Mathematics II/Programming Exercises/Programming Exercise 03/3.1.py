import os
import csv

import numpy as np
import pandas as pd

from pyscipopt import Model, quicksum, multidict


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

def import_csv(allfoods_abs_file_path: str, reference_abs_file_path: str):
    with open(allfoods_abs_file_path, newline='') as csvfile:
            allfoods = csv.DictReader(csvfile, delimiter=';')

    with open(reference_abs_file_path, newline='') as csvfile:
            reference = csv.DictReader(csvfile, delimiter=';')

    return allfoods, reference

def import_csv_pd(allfoods_abs_file_path: str, reference_abs_file_path: str):

    # open csv and convert to dataframe
    with open(allfoods_abs_file_path, newline='') as csvfile:
        allfoods = pd.read_csv(csvfile, sep=";")

    with open(reference_abs_file_path, newline='') as csvfile:
        reference = pd.read_csv(csvfile, sep=";")

    return allfoods, reference

def create_dataset(foods, reference):

    # TODO: reference.reindex([...])

    F = foods["NDB_No"].count()
    N = reference["Nutrient"].count()

    a = np.zeros(N)
    b = np.zeros(N)

    for i in range(N):
        a[i] = reference["Max"][i]
        b[i] = reference["Min"][i]

    n = np.zeros((F, N))

    for j in range(F):
        for i in range(N):
            n[j][i] = 
    return F, N, a, b, 0

def diet_model(F,N,a,b,n):
    """
        - F         : set of foods
        - N         : set of nutrients
        - a[i]      : minimum intake of nutrient i
        - b[i]      : maximum intake of nutrient i
        - n[j][i]   : amount of nutrient i in food j
    """

    model = Model("Diet")

    # define indices for fiber and sugar, respectively
    i_fiber, i_sugar = 5, 6

    # define objective vector c for the objective max c^T*x
    def c(j):
        return (n[i_fiber][j] - n[i_sugar][j])

    # create variables
    x = {}
    for j in F:
        x[j] = model.addVar(vtype="I", name="x(%s)"%j)

    # define constraints:
    for j in F:

        # max amount of nutrient i
        model.addCons(quicksum(n[j][i]*x[j] for i in N) <= b[j])

        # min amount of nutrient i
        model.addCons(quicksum(n[j][i]*x[j] for i in N) >= a[j])

    # objective:
    model.setObjective(quicksum((c[j]*x[j]) for j in F), "maximize")
    model.data = x

    return model

    
if __name__ == "__main__":
    allfoods_abs_file_path, reference_abs_file_path = file_paths()
    allfoods, reference = import_csv_pd(allfoods_abs_file_path, reference_abs_file_path)

    F, N, a, b, n = create_dataset(allfoods, reference)

    #model = diet_model(F, N, a, b, n)
    # model.hideOutput() # silent mode
    #model.optimize()