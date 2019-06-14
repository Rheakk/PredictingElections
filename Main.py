from pytrends.request import TrendReq
import pandas as pd
import logging

trend = TrendReq(hl='en-US', tz=360)


def create_gtrends_df(searchTerms, po):

    region = "US-" + po
    logging.debug ("building for search terms:\n%r", searchTerms)
    trend.build_payload(searchTerms, cat=0, timeframe='2018-10-06 2018-11-06', geo=region, gprop='')
    iot_df = trend.interest_over_time()
    logging.debug("Interest over time df:\n:%r", iot_df)
    pd.set_option('display.max_columns', 10)
    return iot_df




def makeStateDFs(data):

    state_races = {}
    states = data["state"].unique()

    for state in states:
        new_df = data.loc[data['state'] == state]
        new_df = new_df.drop_duplicates(subset="candidate", keep='first')
        state_races[state] = new_df.reset_index()
        # print(state_races[state])

    return state_races



def makeWinnersDf(data):

    all_states = makeStateDFs(data)

    winners_df = pd.DataFrame(columns = ['state', 'winner'])
    i = 0

    for state in all_states:
        winner = all_states[state]['candidatevotes'].idxmax()
        winners_df.loc[i] = [state.lower()] + [str(all_states[state].at[winner, 'candidate']).lower()]
        i=i+1

    return winners_df



def getSearchData(data):

    state_races = makeStateDFs(data)
    google_dfs = {}

    for state in state_races.keys():

        state_df = state_races[state]
        state_po = str(state_df.at[0, 'state_po'])
        candidates = state_races[state]['candidate'].tolist()

        # will have to come up with more encompassing code for larger lists...
        if len(candidates) > 5:

            tempDfs = []
            cands1 = []
            cands2 = []

            logging.debug ("doing first dataframe")
            for i in range(0, 5):
                cands1.append(str(candidates[i]).lower())

            google_df1 = create_gtrends_df(cands1, state_po)
            tempDfs.append(google_df1)

            logging.debug ("doing second dataframe")
            for j in range(5, len(candidates)):
                cands2.append(str(candidates[j]).lower())

            google_df2 = create_gtrends_df(cands2, state_po)
            tempDfs.append(google_df2)

            state_google_df = pd.concat(tempDfs, sort=True)

        else:

            for i in range(0, len(candidates)):
                candidates[i] = str(candidates[i]).lower()

            state_google_df = create_gtrends_df(candidates, state_po)

        google_dfs[state] = state_google_df

    return google_dfs



def getHighestSearched(state_dfs):

    highestSearched = {}
    for state in state_dfs:
        current_df = state_dfs[state]
        searchVols = {}
        columns = list(current_df)
        columns = cleanUp(columns)

        for i in columns:
            total = current_df[i].sum()
            searchVols[i] = total

        topCand = getMostSearchedCand(searchVols)
        highestSearched[state.lower()] = topCand

    return highestSearched



def getMostSearchedCand(dict):

    candidate = next(iter(dict.keys()))
    largest = dict[candidate]

    for name in dict.keys():
        if dict[name] > largest:
            largest = dict[name]
            candidate = name

    # print(candidate, largest)

    return candidate



def cleanUp(list):

    if 'nan' in list:
        list.remove('nan')
    if 'isPartial' in list:
        list.remove('isPartial')
    if 'others' in list:
        list.remove('others')
    return list



def createComparison(data):

    searchVolData = getSearchData(data)
    highestSearched = getHighestSearched(searchVolData)
    comparison_df = makeWinnersDf(data)
    comparison_df["highest_searched"] = ''

    for i in range(0, len(comparison_df.index)):
        for state in highestSearched.keys():
            if comparison_df.at[i, 'state'] == str(state):
                comparison_df.at[i, 'highest_searched'] = highestSearched[state]

    return comparison_df

def identifyMatches(df, col1, col2):

    df['is_a_match'] = ''

    for i in range(0, len(df.index)):
        if df.at[i, col1] == df.at[i, col2]:
            df.at[i, 'is_a_match'] = 'Y'
        else:
            df.at[i, 'is_a_match'] = 'N'

    return df


def main():

    #logging.getLogger().setLevel(logging.INFO)
    #logging.getLogger().setLevel(logging.DEBUG)

    # loading election data
    edata = pd.read_csv("/Users/Rhea/Desktop/senate_election_data")

    data2018 = edata.loc[edata['year'] == 2018]

    compare_df = createComparison(data2018)
    final_df = identifyMatches(compare_df, 'winner', 'highest_searched')
    print(final_df)


main()


