"""
    Author: Rhea Kothari
    Created: 16-June-2019

    module to manage senate election data
"""
from getData import getUrlPd, pdToSql
import logging


def fetchSenateElection ():
    """
        get senate election data - save it in a file and sql db and return as pd

        :return: pandas series with loaded data from the url file
    """

    # Url obtained from
    # https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/PEJ5QU/XXQCIK&version=4.0
    # and then go down and look for the Download URL section. this link can be found there.
    #
    url="https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/PEJ5QU/XXQCIK"

    # output file where the downloaded data will be saved
    electionDataFile = "data/senate_election_data.tab"

    # the download comes down as a tab delimited file, so \t tells pandas.read_csv that the file is a
    # a tab delimited file.
    df = getUrlPd (url, electionDataFile, sep='\t')

    # save the data to a sql db
    dbString = "postgres://rhea@localhost/research"

    pdToSql (df, "state_senate", dbString)

    return df



if __name__ == "__main__":

    logging.basicConfig (
        format='%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s',
        level=logging.DEBUG
    )

    fetchSenateElection ()
