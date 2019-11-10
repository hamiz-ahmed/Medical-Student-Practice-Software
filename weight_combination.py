"""Script containing functions for creating weight combinations"""
from student_practice_pair import StudentPracticePair
import pandas as pd


def create_all_weight_combinations(data_store):
    """
    Create all weight combinations for student practice pairs
    :param data_store:
    :return:
    """
    weight_data = []
    print("Creating all weight combinations..")

    for i, stud_df_row in data_store.df_students.iterrows():
        # first loop iterating through all students
        for j, prac_df_row in data_store.df_practices.iterrows():
            # second loop iterating through all practices

            # initialize a student practice pair
            stud_prac_pair = StudentPracticePair(stud_df_row, prac_df_row)
            s_id = i
            p_id = j

            # get all relevant data
            weight = stud_prac_pair.get_pair_weight()
            stud_addr = stud_prac_pair.get_student_address()
            prac_addr = stud_prac_pair.get_practice_address()
            children = "Yes" if stud_prac_pair.has_children() else "No"
            requires_relocation = stud_prac_pair.requires_relocation()
            travel_mode = stud_prac_pair.get_fastest_transport_mode()
            duration = stud_prac_pair.get_fastest_transport_duration() / 60
            match_speci = ", ".join(
                stud_prac_pair.find_intersecting_specialities())

            # append the data in the list
            weight_data.append(
                [s_id, p_id, weight, stud_addr, prac_addr, requires_relocation,
                 children, travel_mode, duration, match_speci])

    # create a dataframe out of all possible combinations for better
    # querying
    weight_df = pd.DataFrame(weight_data,
                             columns=["s_id", "p_id", "Weight",
                                      "Address of the student",
                                      "Address of the practice",
                                      "Required to move (No, Alternative 1, "
                                      "Alternative 2)",
                                      "Children (Yes, No)",
                                      "Travel Mode (Bicycle, Car)",
                                      "Duration (Minutes)",
                                      "Matching Specialities"])

    # save the dataframe in csv
    weight_df.to_csv("data/all_possible_pairs.csv", sep="\t",
                     index=False)
    print("Combinations created, can be founf at data/all_possible_pairs.csv")

    return weight_df


def extract_best_weights_students(data_store, weight_df):
    """
    Select best student practice pair weight
    :param data_store:
    :param weight_df:
    :return:
    """
    print("Extracting best combinations..")
    max_pairs = []

    for i, stud_df_row in data_store.df_students.iterrows():
        # iterate through rows of students

        # find the row with max pair weight from all combinations
        max_weight_pair_row = \
            weight_df[weight_df.s_id == i].sort_values(by=['Weight'],
                                                       ascending=False).iloc[0]

        # restructure the data
        p_id = max_weight_pair_row['p_id']
        pair_str = str(i) + "<->" + p_id
        max_weight_pair_row = max_weight_pair_row.drop(labels=['s_id', 'p_id'])
        max_weight_pair_row = max_weight_pair_row.set_value("Pair", pair_str)

        max_weight_pair_row = max_weight_pair_row.reindex(
            ["Pair", "Weight", "Address of the student",
             "Address of the practice", "Required to move (No, "
                                        "Alternative 1, Alternative 2)",
             "Children (Yes, No)", "Travel Mode (Bicycle, Car)",
             "Duration (Minutes)", "Matching Specialities"])

        max_pairs.append(max_weight_pair_row)

    # create the dataframe
    best_weights_df = pd.DataFrame(max_pairs)
    best_weights_df.to_csv("data/best_pairs.csv",
                           columns=max_weight_pair_row.index,
                           index=False, sep="\t")
    print("Combinations extracted. Final result can be found "
          "at data/best_pairs.csv")
