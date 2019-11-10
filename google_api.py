"""Script containing necessary functions for fetching result from API"""
import pandas as pd
import googlemaps


class GoogleAPI:

    def __init__(self, api_key=None):
        self.api_key = api_key

    def _data_fetched_already(self, dist_csv):
        """
        Check if duration and distances already exist in the address file
        :param dist_csv:
        :return:
        """
        df_addresses = pd.read_csv(dist_csv, sep="\t")
        if 'distance' and 'duration' in df_addresses.columns:
            print("Data already fetched before. Not calling API")
            return True

        return False

    def fetch_distances_from_api(self, dist_csv):
        """
        Compute distance and durations of already saved address csv file from
        API.

        This method queries the api and
        saves the distances and durations in the already existing
        csv file so that the api doesn't have to be queried again and again.
        :param dist_csv:
        :return:
        """
        # check if api has already been called before
        if not self._data_fetched_already(dist_csv):
            client = googlemaps.Client(key=self.api_key)
            df_addresses = pd.read_csv(dist_csv, sep="\t")

            dists = []
            durations = []
            print("Calling API...")

            # iterate over all the addresses of the dataframe and query the api
            # iteratively
            for index, df_row in df_addresses.iterrows():
                origin = df_row['stud_add']
                dest = df_row['prac_add']

                if df_row['is_car']:
                    mode = "driving"
                else:
                    mode = "bicycling"

                # query the api
                matrix = client.distance_matrix(origin, dest,
                                                mode=mode)
                dist_metrs = matrix['rows'][0]['elements'][0]["distance"][
                    'value']
                duration_secs = matrix['rows'][0]['elements'][0]["duration"][
                    'value']

                # append extracted values from api in a list
                dists.append(dist_metrs)
                durations.append(duration_secs)

            # add these list in the dataframe
            df_addresses['distance'] = dists
            df_addresses['duration'] = durations

            # save the dataframe back to its place
            df_addresses.to_csv(dist_csv, sep='\t', index=False)

            print("Durations fetched.")
