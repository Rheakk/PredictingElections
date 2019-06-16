import logging
#import psycopg2 as sql
import sqlalchemy as sql
import pandas.io.sql as psql
import pandas as pd

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

for row in engine.execute ("select * from Person"):
    logging.info ("%r", row)



df = psql.read_sql ("select * from Person", engine)
logging.info ("Read Person:\n%r", df)

# save this df in a table by the name pd_person
df.to_sql ("pd_person", engine, if_exists='replace')
# read it to see if it worked
df2 = psql.read_sql ("select * from pd_person", engine)
logging.info ("Read pd_person:\n%r", df)

