from pytrends.request import TrendReq
import pandas as pd

trend = TrendReq(hl='en-US', tz=360)

# build payload
kw_list = ["dianne feinstein", "kevin de leon"]
trend.build_payload(kw_list, cat=0, timeframe='2018-10-06 2018-11-06', geo='', gprop='')

# Interest Over Time
interest_over_time_df = trend.interest_over_time()
# print(interest_over_time_df)
# print("*****************")

print()

# print (trends.suggestions("trump"))

# print(trends.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=1, day_end=30, hour_end=23, cat=0, geo='', gprop='', sleep=60))

# loading and printing election data
edata = pd.read_csv("/Users/Rhea/Desktop/senate_election_data")
#print(edata)

print()

# extract winners from each state senate election
def extractWinners(start, end):

    winners_df = pd.DataFrame(columns=["state", "winner_index"])

    winners = []
    winner = None
    curState = None

    for i in range(start, end + 1):
        nextState = edata.at[i, "state"]

        if (curState == nextState):

            curCandVotes = edata.at[i, "candidatevotes"]

            if curCandVotes > topVotes:
                topVotes = curCandVotes
                winner = i

        else:
            if winner is not None:
                dict = {curState : winner}
                winners.append(dict)
            curState = nextState
            winner = i
            topVotes = edata.at[i, "candidatevotes"]

    winners.append({curState : winner})
    print(winners)
    print(len(winners))

    for i in range(0,len(winners)):
        winners_df.loc[i] = [winners[i].keys()] + [winners[i].values()]
    print(winners_df)

#    for winner in winners:
#        print (edata.iloc[winner])
#        print ("------------")

    return winners

extractWinners(3269, 3420)
print()

# extract all midterm election candidates per state
def extractCandidates(start, end):

    states = {}
    cands = set()
    curState = edata.at[start, "state"]

    for i in range(start, end + 1):

        nextState = edata.at[i, "state"]
        cand = str(edata.at[i, "candidate"]).lower()

        if (curState == nextState):
            if (cand not in cands):
                cands.add(cand)

        else:
            states[curState.lower()] = cands
            states[nextState.lower()] = []
            cands = set()
            if cand not in cands:
                cands.add(cand)
            curState = nextState

    states[curState.lower()] = cands
    for state in states:
        print(state, states[state])
    return states

# extractCandidates(3269, 3420)

# create dataframe given list of search terms
def createDf(searchTerms):

    trend.build_payload(searchTerms, cat=0, timeframe='2018-10-06 2018-11-06', geo='US', gprop='')
    iot_df = trend.interest_over_time()
    pd.set_option('display.max_columns', 10)
    return iot_df

state_races = extractCandidates(3269, 3420)
list = []

print(createDf(state_races["wisconsin"]))
# print(createDf(state_races["iowa"]))

# creating list of dataframes for each state's midterm gtrends data
# searchVolData = []
# allRaces = extractCandidates(3269, 3420)
# for race in allRaces:
#     searchVolData.append(createDf(allRaces[race]))
# for dataframe in searchVolData:
#     print(dataframe)

#extractWinners(3269, 3420)
print()

