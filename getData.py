import os.path
import logging
from urllib import request
import pandas as pd


def fetchData (url, out_path, sep=','):
    ''' get data from url which is used to to be a link downloadable data
    '''

    # if the file already exists then do not download. and use existing downloaded
    # file
    if os.path.isfile(out_path):
        logging.info("Filename %s already downloaded", out_path)
    else:
        logging.info("downloading using %s", url)
        try:
            request.urlretrieve(url, out_path)
        except:
            logging.exception ("Could not download url:%s into %s", url, out_path)
            exit(1)
        logging.info("downloaded %s", out_path)

    data = pd.read_csv(out_path, sep=sep)
    logging.debug("Loaded data:\n%r", data.head())

    return data

def fetchSenateElection ():
    """
        get senate election data using fetchData
    :return: pandas series with loaded data from the url file
    """

    # Url obtained from
    # https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/PEJ5QU/XXQCIK&version=4.0
    # and then go down and look for the Download URL section. this link can be found there.
    #
    url="https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/PEJ5QU/XXQCIK"

    # output file where the downloaded data will be saved
    senate_election_file = "data/senate_election_data.tab"

    # the download comes down as a tab delimited file, so \t tells pandas.read_csv that the file is a
    # a tab delimited file.
    return fetchData  (url, senate_election_file, sep='\t')



if __name__ == "__main__":

    logging.getLogger().setLevel(logging.DEBUG)

    fetchSenateElection ()
