"""Script containing class for handling all data related functions"""
import pandas as pd
import os


class DataStore:
    """Class incorporating functions for extracting students and practices."""

    def __init__(self):
        """
        Initialize the datastore with two df variables.
        """
        self.df_practices = pd.DataFrame()
        self.df_students = pd.DataFrame()

    def clear(self):
        """
        Clears the datastore.
        :return:
        """
        self.df_practices = None
        self.df_students = None

    def get_practices(self):
        """
        Gets saved practices dataframe.
        :return:
        """
        return self.df_practices

    def get_students(self):
        """
        Gets saved students dataframe
        :return:
        """
        return self.df_students

    def read_practices_from_csv_file(self, practice_csv_file):
        """
        Reads the practices from csv file and stores it in the variable
        self.df.practices.
        :param practice_csv_file:
        :return:
        """
        df = pd.read_csv(practice_csv_file, sep="\t")
        self.df_practices = df.set_index("id")

    def read_students_from_csv_file(self, student_csv_file):
        """
        Reads the students from csv file and stores it in the variable
        self.df.students
        :param student_csv_file:
        :return:
        """
        df = pd.read_csv(student_csv_file, sep="\t")
        self.df_students = df.set_index("id")

    def extract_addresses(self, stud_df, pract_df, is_bike):
        """
        Methdod to extract all addresses of students including alternate
        addresses of the students and make combinations against all practice
        adresses.

        This method helps to create a new address csv file from which addresses
        can be directly queried using student address as the source and
        practice address as the destination address. Returns a list of
        student addresses against practice addresses
        :param stud_df: df
        :param pract_df: df
        :param is_bike: if True, all combinations will be made considering
        bike as the mode of transport even for people having car
        :return: list
        """
        addr_list = []
        # make bike combinations even for people having car
        has_car = 0

        if not is_bike:
            # make combinations for people having car only
            stud_df = stud_df[stud_df['hasCar'] == 1]
            has_car = 1

        for i in range(len(stud_df)):
            stud_df_row = stud_df.loc[stud_df.index[i]]

            for j in range(len(pract_df)):
                pract_df_row = pract_df.loc[pract_df.index[j]]

                # main address against practice address
                df_list_main = [stud_df_row['address'],
                                pract_df_row['address'],
                                has_car]
                addr_list.append(df_list_main)

                # alternate address against practice address
                if not pd.isna(stud_df_row['alternativeAddress1']):
                    df_list_main = [stud_df_row['alternativeAddress1'],
                                    pract_df_row['address'],
                                    has_car]
                    addr_list.append(df_list_main)

                if not pd.isna(stud_df_row['alternativeAddress2']):
                    df_list_main = [stud_df_row['alternativeAddress2'],
                                    pract_df_row['address'],
                                    has_car]
                    addr_list.append(df_list_main)
        return addr_list

    def create_address_csv_file(self):
        """
        Creates the csv file addresses.csv by making all possible combinations
        of student addresses against practice addresses.
        :return:
        """
        print("Creating addresses.csv file")

        if os.path.isfile("data/addresses.csv"):
            print("Address file already exists")
            return

        bike_addr_list = self.extract_addresses(self.df_students,
                                                self.df_practices,
                                                is_bike=True)
        car_addr_list = self.extract_addresses(self.df_students,
                                               self.df_practices,
                                               is_bike=False)

        df = pd.DataFrame(bike_addr_list + car_addr_list,
                          columns=['stud_add', 'prac_add', 'is_car'])

        df.to_csv("data/addresses.csv", sep="\t", index=False)
        print("File saved at data/addresses.csv")
