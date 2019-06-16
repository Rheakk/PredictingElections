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

def pdToSql (df, table, dbString):
    '''
    save pandas dataFrame to an sql db table

    :param df: pandas data frame to be saved as a SQL table
    :param table: table name where to save the data in
    :param dbString: sql engine db string.
    :return: True if save successful else returns False
    '''

    import sqlalchemy as sql

    engine = sql.create_engine(dbString)

    logging.debug ("Saving dataframe:%s to sql table:%s", df.head(), table)

    df.to_sql (table, engine, if_exists='replace')

    logging.info ("Saved dataframe to sql table:%s", table)

    return True
