import logging
import sqlalchemy as sql
import pandas.io.sql as psql

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

sqlStr = '''
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

# sample of how to read from sql db into python list
#for row in engine.execute (sqlStr):
#    logging.info ("%r", row)

# sample of how to read from sql db into pandas df
df = psql.read_sql (sqlStr, engine)
logging.info ("%r", df)


# save this df in a table by the name pd_person
#df.to_sql ("pd_person", engine, if_exists='replace')
# read it to see if it worked
#df2 = psql.read_sql ("select * from pd_person", engine)
#logging.info ("Read pd_person:\n%r", df)

