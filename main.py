"""Main entry point for the program"""

from data_store import DataStore
from google_api import GoogleAPI
import weight_combination
import json


def get_api_key():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    return data['api_key']


def execute_pipeline():
    """
    Executes and calls all necessary functions to run the program.
    :return:
    """
    api_key = get_api_key()

    # create datastore
    ds = DataStore()

    # read csv files
    ds.read_practices_from_csv_file("data/practices.csv")
    ds.read_students_from_csv_file("data/students.csv")

    # # create address combination file
    ds.create_address_csv_file()

    # fetch distance and duration from Google API
    GoogleAPI(api_key=api_key).fetch_distances_from_api('data/addresses.csv')

    # create all weight combination file
    weight_df = weight_combination.create_all_weight_combinations(ds)

    # extract best possible weight combinations
    weight_combination.extract_best_weights_students(ds, weight_df)


if __name__ == "__main__":
    execute_pipeline()
