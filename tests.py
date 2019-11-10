import unittest
from data_store import DataStore
from student_practice_pair import StudentPracticePair
from google_api import GoogleAPI


class DataStoreTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(DataStoreTests, self).__init__(*args, **kwargs)
        self.ds = DataStore()

    def test_read_practices_from_csv_file(self):
        # read practices test file
        self.ds.read_practices_from_csv_file("data/test_data/practices.csv")

        # extract addresses
        address1 = self.ds.df_practices.iloc[0]['address']
        address2 = self.ds.df_practices.iloc[1]['address']

        # check if they are correct
        self.assertEqual(address1,
                         'Rhaban-Fröhlich-Straße 11, 60433 Frankfurt am Main')
        self.assertEqual(address2,
                         'Kurmainzer Straße 160, 65936 Frankfurt am Main')

    def test_read_students_from_csv_file(self):
        # read students test file
        self.ds.read_students_from_csv_file("data/test_data/students.csv")

        # extract addresses
        address1 = self.ds.df_students.iloc[0]['address']
        address2 = self.ds.df_students.iloc[1]['address']

        # check if they are correct
        self.assertEqual(address1,
                         'Am Waldacker 21c, 60388 Frankfurt am Main')
        self.assertEqual(address2,
                         'Storchgasse 2, 65929 Frankfurt am Main')

    def test_extract_addresses(self):
        self.ds.read_students_from_csv_file("data/test_data/students.csv")
        self.ds.read_practices_from_csv_file("data/test_data/practices.csv")

        bike_list = self.ds.extract_addresses(self.ds.get_students(),
                                              self.ds.get_practices(),
                                              is_bike=True)
        car_list = self.ds.extract_addresses(self.ds.get_students(),
                                             self.ds.get_practices(),
                                             is_bike=False)

        # the main address of student against practice address 0
        self.assertEqual(bike_list[0],
                         ['Am Waldacker 21c, 60388 Frankfurt am Main',
                          'Rhaban-Fröhlich-Straße 11, 60433 Frankfurt am Main',
                          0])

        self.assertEqual(bike_list[1], ['Pforzheimer Straße 15, '
                                        '60329 Frankfurt am Main',
                                        'Rhaban-Fröhlich-Straße 11, '
                                        '60433 Frankfurt am Main', 0])

        self.assertEqual(len(car_list), 0)


class StudentPracticePairTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(StudentPracticePairTests, self).__init__(*args, **kwargs)
        self.ds = DataStore()
        self.ds.read_students_from_csv_file("data/test_data/students.csv")
        self.ds.read_practices_from_csv_file("data/test_data/practices.csv")
        self.pair = StudentPracticePair(
            self.ds.df_students.loc['S001'],
            self.ds.df_practices.loc['P001'],
            address_path="data/test_data/addresses.csv")

    def test_fetch_travel_duration(self):
        dur = self.pair._fetch_travel_duration(self.pair.student['address'],
                                               has_car=0)
        self.assertEqual(dur, 2207)

    def test_fetch_durations_for_all_addresses(self):
        self.assertEqual(len(self.pair.durations.keys()), 3)
        self.assertEqual(self.pair.durations['main_duration0'], 2207)

    def test_find_intersecting_specialities(self):
        spec = self.pair.find_intersecting_specialities()
        self.assertEqual(spec[0], 'notfallmedizin')

    def test_has_children(self):
        has_children = self.pair.has_children()
        self.assertEqual(has_children,
                         self.ds.df_students.loc['S001']['hasChildren'])

    def test_get_student_address(self):
        pair = StudentPracticePair(self.ds.df_students.loc['S001'],
                                   self.ds.df_practices.loc['P001'],
                                   address_path="data/test_data/addresses.csv")
        self.assertEqual(pair.get_student_address(),
                         "Im Wörth 8, 60433 Frankfurt am Main")

    def test_get_practice_address(self):
        self.assertEqual(self.pair.get_practice_address(),
                         "Rhaban-Fröhlich-Straße 11, 60433 Frankfurt am Main")

    def test_get_fastest_transport_duration(self):
        dur = self.pair.get_fastest_transport_duration()
        self.assertEqual(dur, 116)

    def test_get_fastest_transport_mode(self):
        mode = self.pair.get_fastest_transport_mode()
        self.assertEqual(mode, "bicycle")

    def test_requires_relocation(self):
        self.assertEqual(self.pair.requires_relocation(), "Alternative 2")


class GoogleApiTests(unittest.TestCase):

    def test_data_fetched_already(self):
        google = GoogleAPI()
        value = google._data_fetched_already("data/test_data/addresses.csv")
        self.assertTrue(value)


if __name__ == '__main__':
    unittest.main()
