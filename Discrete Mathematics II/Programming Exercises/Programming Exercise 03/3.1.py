from cmath import nan
import os
import csv

import numpy as np
import pandas as pd

from pyscipopt import Model, quicksum


def file_paths():
    """
    Sets the file paths
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
    """
    Opens csv and converts to Pandas DataFrame
    """
    with open(allfoods_abs_file_path, newline='') as csvfile:
        allfoods = pd.read_csv(csvfile, sep=";")

    with open(reference_abs_file_path, newline='') as csvfile:
        reference = pd.read_csv(csvfile, sep=";")

    return allfoods, reference

def create_dataset(foods: pd.DataFrame, reference: pd.DataFrame):
    """
    Creates datasets for further use in the model
    """
    def data_cleanup(foods: pd.DataFrame, reference: pd.DataFrame):
        """
        Performs cleanup of foods, reference s. t. layout matches for further computation
        """

        # add rows "Water", "Total Sugar"
        reference.loc[30] = (["Water", "g", None, None])
        reference.loc[31] = (["Total Sugar", "g", None, None])
        
        # reorder rows to match "allfoods.csv"
        reference = reference.reindex([30, 0, 2, 1, 6, 7, 31, 22, 25, 24, 23, 21, 20, 26, 28, 29, 27, 19, 12, 13, 14, 17, 15, 16, 18, 8, 10, 9, 11, 3, 4, 5]).reset_index()

        return foods, reference

    foods, reference = data_cleanup(foods, reference)

    F = foods["NDB_No"].count()
    N = reference["Nutrient"].count()

    a = np.zeros(N)
    b = np.zeros(N)

    for i in range(N):
        a[i] = reference["Min"][i]
        b[i] = reference["Max"][i]

    n = np.delete(foods.to_numpy(), [0, 1], 1)

    print(b)

    return F, N, a, b, n

def diet_model(F,N,a,b,n):
    """
        - F         : number of foods
        - N         : number of nutrients
        - a[i]      : minimum intake of nutrient i
        - b[i]      : maximum intake of nutrient i
        - n[j][i]   : amount of nutrient i in food j
    """

    model = Model("Diet")

    # define indices for fiber and sugar, respectively
    i_fiber, i_sugar = 5, 6

    # define objective vector c for the objective [ max c^T*x ]
    sugar, fiber = np.zeros(F), np.zeros(F)
    for j in range(F):
        sugar[j] = n[j][i_sugar]
        fiber[j] = n[j][i_fiber]

    # create variables
    x = {}
    for j in range(F):
        x[j] = model.addVar(vtype="C", name="x(%s)"%j)

    # define constraints:
    cons = {}
    for i in range(N):
        cons[i] = model.addCons(quicksum(n[j][i]*x[j] for j in range(F)) <= b[i], name="Nutr(%s)"%i)
        model.chgLhs(cons[i], a[i])

    # objective:
    model.setObjective(quicksum((fiber[j]*x[j] - sugar[j]*x[j]) for j in range(F)), "maximize")
    model.data = x

    return model

    
if __name__ == "__main__":
    allfoods_abs_file_path, reference_abs_file_path = file_paths()
    allfoods, reference = import_csv_pd(allfoods_abs_file_path, reference_abs_file_path)

    F, N, a, b, n = create_dataset(allfoods, reference)

    model = diet_model(F, N, a, b, n)

    #model.hideOutput() # silent mode
    model.optimize()

    #x = model.data
    #for j in x:
    #    print(model.getVal(x[j]))