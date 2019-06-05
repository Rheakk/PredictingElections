from pytrends.request import TrendReq
import pandas as pd

pytrend = TrendReq(hl='en-US', tz=360)

#build payload
kw_list = ["dianne feinstein", "kevin de leon"]
pytrend.build_payload(kw_list, cat=0, timeframe='2018-01-01 2018-11-30', geo='', gprop='')

# Interest Over Time
interest_over_time_df = pytrend.interest_over_time()
print(interest_over_time_df)

# print (pytrends.suggestions("trump"))

# print(pytrends.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=1, day_end=30, hour_end=23, cat=0, geo='', gprop='', sleep=60))


# loading election data
edata = pd.read_csv("/Users/Rhea/Desktop/senate_election_data")
print(edata)
