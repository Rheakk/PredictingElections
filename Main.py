import logging
from pytrends.request import TrendReq
import pandas as pd
from electionData import fetchSenateElection

# extract winners from each state senate election
def extractWinners(edata, start, end):

    winners = []
    winner = edata.at[start, "candidate"]
    curState = edata.at[start, "state"]
    topVotes = edata.at[start, "candidatevotes"]

    for i in range(start, end + 1):
        nextState = edata.at[i, "state"]

        if (curState == nextState):

            curCandVotes = edata.at[i, "candidatevotes"]

            if curCandVotes > topVotes:
                topVotes = curCandVotes
                winner = edata.at[i, "candidate"]

        else:
            winners.append(winner)
            curState = nextState
            winner = edata.at[i, "candidate"]
            if (i != end):
                topVotes = edata.at[i, "candidatevotes"]

    for winner in winners:
        print (winner)

    return winners


# extract all midterm election candidates per state
def extractCandidates(edata, start, end):

    states = {}
    cands = []
    curState = edata.at[start, "state"]

    for i in range(start, end + 1):

        #TODO: The logic below can be simpler/cleaner
        # for example can probably check if a state does not
        # exists in the states and then add states[state] = []
        # and then just append always.

        nextState = edata.at[i, "state"]
        cand = edata.at[i, "candidate"]

        states[nextState] = []

        if (curState == nextState):
            # make sure to add a candidate just once, otherwise
            # gtrends to fails to send data if it finds duplicates.
            if cand not in cands:
                cands.append(cand)
        else:
            states[curState] = cands
            states[nextState] = []
            cands = []
            cands.append(cand)
            curState = nextState

    return states

# create dataframe given list of search terms
def createDf(searchTerms):

    logging.debug ("building for search terms:\n%r", searchTerms)
    trend.build_payload(searchTerms, cat=0, timeframe='2018-01-01 2018-11-30', geo='', gprop='')
    iot_df = trend.interest_over_time()
    return iot_df


if __name__ == "__main__":

    # uncommend DEBUG to see more logging/debuggin info that will
    # tell what the program is doing in more details.
    # once tested and works well, then you leave INFO
    #logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)

    trend = TrendReq(hl='en-US', tz=360)

    # build payload
    kw_list = ["dianne feinstein", "kevin de leon"]
    trend.build_payload(kw_list, cat=0, timeframe='2018-01-01 2018-11-30', geo='', gprop='')

    # Interest Over Time
    interest_over_time_df = trend.interest_over_time()
    logging.debug("Interest over time df:\n:%r", interest_over_time_df)


    # print (trends.suggestions("trump"))
    # print (trends.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0,
    # year_end=2018, month_end=1, day_end=30, hour_end=23, cat=0, geo='', gprop='', sleep=60))

    # loading and printing election data
    edata = fetchSenateElection()


    # creating list of dataframes for each state's midterm gtrends data
    searchVolData = []
    allRaces = extractCandidates(edata, 3269, 3420)
    for race in allRaces:
        dataFrame = createDf(allRaces[race])
        searchVolData.append(dataFrame)
        logging.info("candidates dataFrame:\n%r:", dataFrame.head())

    winData = extractWinners(edata, 3269, 3420)
    logging.info ("Winners:\n%r", winData)

