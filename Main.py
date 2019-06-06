from pytrends.request import TrendReq
import pandas as pd

trend = TrendReq(hl='en-US', tz=360)

# build payload
kw_list = ["dianne feinstein", "kevin de leon"]
trend.build_payload(kw_list, cat=0, timeframe='2018-01-01 2018-11-30', geo='', gprop='')

# Interest Over Time
interest_over_time_df = trend.interest_over_time()
print(interest_over_time_df)

print()

# print (trends.suggestions("trump"))

# print(trends.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=1, day_end=30, hour_end=23, cat=0, geo='', gprop='', sleep=60))

# loading and printing election data
edata = pd.read_csv("/Users/Rhea/Desktop/senate_election_data")
print(edata)

print()

# extract winners from each state senate election
def extractWinners(start, end):

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

    return winners

extractWinners(3269, 3420)

