"""Script containing class for a combination of student and practice pairs."""
import pandas as pd


class StudentPracticePair:
    """Class incorporating pairs of student and practice pandas instances."""

    def __init__(self, student, practice, address_path='data/addresses.csv'):
        """
        Intialize the student and practice instance.
        :param student: student series instance
        :param practice: practice series instance
        :param address_path: file path for address file
        """
        self.student = student
        self.practice = practice
        self.addresses_df = pd.read_csv(address_path, sep="\t")
        self.durations = {}
        self.fetch_durations_for_all_addresses()

    def _fetch_travel_duration(self, stud_add, has_car):
        """
        Fetch the travel duration.

        Fetches the travel duration of a particular student address against
        the address of practice
        :param stud_add: Address of the student
        :param has_car: fetch duration for car or bike
        :return:
        """
        prac_address = self.get_practice_address()
        duration = self.addresses_df[
            (self.addresses_df['stud_add'] == stud_add)
            & (self.addresses_df['prac_add'] == prac_address)
            & (self.addresses_df['is_car'] == has_car)]['duration'].tolist()[0]

        return duration

    def _find_max_travel_duration(self):
        return self.addresses_df['duration'].max()

    def _compute_durations_on_diff_addrs(self, stud_address, stud_alternate_1,
                                         stud_alternate_2, has_car):
        """
        Helper method to fetch durations for all addresses of the student.
        :param stud_address:
        :param stud_alternate_1:
        :param stud_alternate_2:
        :param has_car:
        :return:
        """
        main_duration = self._fetch_travel_duration(stud_address,
                                                    has_car)
        self.durations['main_duration' + str(has_car)] = main_duration

        if not pd.isna(stud_alternate_1):
            alter_duration1 = self._fetch_travel_duration(stud_alternate_1,
                                                          has_car)
            # add has_car in key so that keys do not override
            # All bicycle durations will have 0 at the end of the key
            # and all car durations will have 1 at the end of the key
            self.durations['alter_duration1' + str(has_car)] = alter_duration1

        if not pd.isna(stud_alternate_2):
            alter_duration2 = self._fetch_travel_duration(stud_alternate_2,
                                                          has_car)
            self.durations['alter_duration2' + str(has_car)] = alter_duration2

    def fetch_durations_for_all_addresses(self):
        """
        Fetch travel durations for all addresses of a student against the
        practice including the alternate addresses.

        The method is a wrapper for calling calculate_travel_durations for bike
        and car. Hence, if a student has a car, his durations for both bike
        and car are calculated, else only durations for the bike are calculated
        :return:
        """
        stud_address = self.student['address']
        stud_alternate_1 = self.student['alternativeAddress1']
        stud_alternate_2 = self.student['alternativeAddress2']

        has_car = self.student['hasCar']

        # compute bike travel durations
        self._compute_durations_on_diff_addrs(stud_address, stud_alternate_1,
                                              stud_alternate_2, 0)
        if has_car:
            # student has car hence compute durations for car too
            self._compute_durations_on_diff_addrs(stud_address,
                                                  stud_alternate_1,
                                                  stud_alternate_2, 1)

    def find_intersecting_specialities(self):
        """
        Find the list common specialities between student and practice.
        :return: specialities list
        """
        if pd.isna(self.practice['specialties']):
            # no practice specialities
            return []
        else:
            # split the string to list
            specialities_stud = self.student['favoriteSpecialties'].split(',')
            specialities_prac = self.practice['specialties'].split(',')

            # convert them to lowercase and strip off any whitespace
            specialities_prac = [x.lower().strip() for x in specialities_prac]
            specialities_stud = [x.lower().strip() for x in specialities_stud]

            # find the intersection between practice and student specialities
            matching = list(set(specialities_prac) & set(specialities_stud))
            return matching

    def get_pair_weight(self):
        """
        Computes the weight of the pair by fetching different criterias.

        The weight is computed using duration, specialities and children. The
        duration takes in to account the shortest time it takes for a student
        to reach a practice by bike, or if by car. In the end, all criterias
        are given a specific weight to compute the final weight. The duration
        gets a weight of 50, each matching speciality is given a weight of 20
        and whether a person has children or not is assigned a weight of 20.
        :return:
        """
        duration_weight = self._find_max_travel_duration() - self.\
            get_fastest_transport_duration()
        match_specialities = len(self.find_intersecting_specialities())
        children = self.has_children()

        weight = ((0.2 * duration_weight) + (99 * match_specialities) +
                  (0.8 * children)) / 100
        return weight

    def has_children(self):
        """
        Check if a student has children or not.
        :return:
        """
        return self.student['hasChildren']

    def requires_relocation(self):
        """
        Compares the student main address with the shortest duration address
        and returns an answer
        :return:
        """
        stud_addr = self.get_student_address()
        if stud_addr == self.student['address']:
            return "No"
        if stud_addr == self.student['alternativeAddress1']:
            return "Alternative 1"
        if stud_addr == self.student['alternativeAddress2']:
            return "Alternative 2"

    def get_student_address(self):
        """
        Fetch address of the student with the shortest duration to practice.
        :return:
        """
        min_key = min(self.durations, key=self.durations.get)

        if min_key.startswith("main"):
            return self.student['address']

        elif min_key.startswith("alter_duration1"):
            return self.student['alternativeAddress1']

        else:
            return self.student['alternativeAddress2']

    def get_practice_address(self):
        """
        Fetch the address of the practice
        :return:
        """
        return self.practice['address']

    def get_fastest_transport_duration(self):
        """
        Get the shortest transport duration considering all the addresses
        of the student against the practice.
        :return:
        """
        return min(self.durations.values())

    def get_fastest_transport_mode(self):
        """
        Check which transport is fastest, bike or car.
        :return:
        """
        # find the key of the minimum value
        min_key = min(self.durations, key=self.durations.get)

        # all bicycle travel durations have a zero appended in their key
        if min_key.endswith('0'):
            return "bicycle"
        else:
            return "Car"
