from pytrends.request import TrendReq
import pandas as pd
import logging
import sqlalchemy as sql
import pandas.io.sql as psql
import string
import re

logging.basicConfig(
    level=logging.DEBUG,
    format= '%(asctime)s %(filename)s:%(lineno)d %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

try:
    #conStr = "dbname='research' user='rhea'"
    #conn = sql.connect(conStr)
    conStr = "postgres://rhea@localhost/research"
    engine = sql.create_engine (conStr)
except:
    logging.fatal ("Could not connect to db:%s", conStr)

logging.info ("Connected to db:%s", conStr)

def getWinners():

    max_votes_str = '''
    UPDATE state_senate SET candidate = LOWER(candidate);
    select a.* from state_senate a
    INNER JOIN (
	    select state, max (candidatevotes) maxvotes from state_senate
	    where year = 2018
	    group by state
    ) b
    on a.state = b.state and a.candidatevotes = b.maxVotes
    where a.year = 2018
    order by state asc
    '''

    df = psql.read_sql(max_votes_str, engine)
    df.to_sql("winners", engine, if_exists='replace')

    pd.set_option('display.max_columns', 20)
    pd.set_option('display.max_rows', 30)
    logging.info("%", df)

def getCands():

    state_sql_str = '''
        UPDATE state_senate SET candidate = LOWER(candidate);
        select a.year, a.state, a.candidate, a.candidatevotes, a.state_po from state_senate a
        where a.year = 2018
        order by state asc
    '''

    df = psql.read_sql(state_sql_str, engine)
    logging.info("%r", df)

    for index, row in df.iterrows():
        cand = str(row['candidate'])
        df.at[index, 'candidate'] = simplifyNames(cand)

    df = cleanData(df)

    pd.set_option('display.max_columns', 20)
    pd.set_option('display.max_rows', 200)

    return df

def simplifyNames(str):

    # removing punctuation
    newstr = str.translate(str.maketrans('', '', string.punctuation))

    # removing extra descriptions/middle initials
    newstr = re.sub(' [a-z] ', ' ', newstr)
    newstr = re.sub('iii', '', newstr)
    newstr = re.sub('jr', '', newstr)
    newstr = newstr.strip()

    # removing middle names
    asList = newstr.split()
    keep = [asList[0], asList[len(asList) - 1]]
    newstr = " ".join(keep)

    return newstr

def cleanData(df):

    df = df.drop_duplicates(subset="candidate", keep='first')
    df = df[df.candidate != 'None']
    df = df[df.candidate != 'others']
    df = df[df.candidate != 'none of these candidates']
    df = df[df.candidate != 'None None']
    df = df[df.candidate != 'isPartial']

    return df


trend = TrendReq(hl='en-US', tz=360)

def create_gtrends_df(searchTerms, po):

    region = "US-" + po
    logging.debug ("building for search terms:\n%r", searchTerms)
    trend.build_payload(searchTerms, cat=0, timeframe='2018-10-06 2018-11-06', geo=region, gprop='')
    iot_df = trend.interest_over_time()
    logging.debug("Interest over time df:\n:%r", iot_df)
    pd.set_option('display.max_columns', 10)
    return iot_df


def saveSearchData(df):

    states = df['state'].unique().tolist()
    final_df = pd.DataFrame()

    for state in states:

        state_df = df.loc[df['state'] == state].reset_index()

        po = state_df.at[0, 'state_po']

        candidates = list(state_df['candidate'])

        for section in split(candidates, 5):

            google_df = create_gtrends_df(section, po)
            logging.debug ("%s", google_df)
            final_df = pd.concat([final_df, google_df], axis=1)

    final_df.to_sql("google_data", engine, if_exists='replace')


def organizeSearchData():

    raw_df = psql.read_sql('select * from google_data', engine)

    new_df = pd.DataFrame(columns=["date", "candidate", "search_vol"])
    tmp_df = pd.DataFrame(columns=["date", "candidate", "search_vol"])

    cols = raw_df.columns.tolist()
    cols.remove(cols[0])

    for col in cols:

        for i in range(0, len(raw_df.index)):

            tmp_df.loc[i] = [raw_df.at[i, 'date']] + [str(col)] + [str(raw_df.at[i, col])]

        new_df = new_df.append(tmp_df)

    new_df = new_df.reset_index()
    print(new_df)
    new_df.to_sql("google_data", engine, if_exists='replace')

def split(list, n):

    for i in range(0, len(list), n):
        yield list[i:i + n]

def getMostSearched():

    merge_str = '''
        
        SELECT
        category, year, week, value, 
        sum(value) OVER (PARTITION BY category 
            ORDER BY year, week 
            ROWS 2 PRECEDING) AS retention_value_3_weeks
        FROM
            t 
        ORDER BY
            category, year, week ;
    
    
    select a.* from google_search_data a
    INNER JOIN (
	    select state, max (candidatevotes) maxvotes from state_senate
	    where year = 2018
	    group by state
    ) b
    on a.state = b.state and a.candidatevotes = b.maxVotes
    where a.year = 2018
    order by state asc   
    '''



def main():

    #cands = getCands()
    #saveSearchData(cands)
    organizeSearchData()
    #getWinners()

main()




