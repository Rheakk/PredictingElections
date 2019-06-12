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

    winners_df = pd.DataFrame(columns = ['state', 'candidate_idx', 'name'])
    i = 0

    for state in all_states:
        winner = all_states[state]['candidatevotes'].idxmax()
        winners_df.loc[i] = [state.lower()] + [winner] + [all_states[state].at[winner, 'candidate']]
        i=i+1

    return winners_df



def getMostSearched(data):

    state_races = makeStateDFs(data)

    for state in state_races:

        searchVols = {}
        state_df = state_races[state]
        state_po = str(state_df.at[0, 'state_po'])
        candidates = state_races[state]['candidate'].tolist()
        for i in range(0, len(candidates)):
           candidates[i] = str(candidates[i]).lower()
        state_google_df = create_gtrends_df(candidates, state_po)
        columns = list(state_google_df)

        for i in columns:
                total = state_google_df[i].sum()
                searchVols[i] = total

        print(searchVols)


def main():

    #logging.getLogger().setLevel(logging.INFO)
    # logging.getLogger().setLevel(logging.DEBUG)

    # loading election data
    edata = pd.read_csv("/Users/Rhea/Desktop/senate_election_data")

    data2018 = edata.loc[edata['year'] == 2018]
    MichiganData = edata.loc[(edata['year'] == 2018) & (edata['state'] == 'Michigan')]
    ConnecticutData = edata.loc[(edata['year'] == 2018) & (edata['state'] == 'Connecticut')]

    getMostSearched(data2018)

main()


