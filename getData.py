"""
    Author: Rhea Kothari
    Created: 16-June-2019

    A common module that allows for downloading of files from url.

    Also will will return as Pandas Data Frame and save data to sql database
"""
import os.path
import logging
from urllib import request
import pandas as pd


def saveUrl (url, outPath, sep=','):
    '''
        get data from url which is a link to downloadable data file

        outPath - is the path of the filename where data needs to be saved

        returns outPath of the file downloaded.
    '''

    # if the file already exists then do not download. and use existing downloaded
    # file
    if os.path.isfile(outPath):
        logging.info("Filename %s already downloaded", outPath)
    else:
        logging.info("downloading using %s", url)
        try:
            request.urlretrieve(url, outPath)
        except Exception as ex:
            logging.exception ("Could not download url:%s into %s", url, outPath)
            raise ex

    logging.info("downloaded %s", outPath)
    return outPath

def getUrlPd (url, outPath, sep=','):
    '''
        get data from url which is a link downloadable data file and returns
        as a pandas data frame

        sep in the file for parsing - e.g. '\t' for a tab delimited file
    '''

    urlFile = saveUrl (url, outPath)

    data = pd.read_csv(urlFile, sep=sep)

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
