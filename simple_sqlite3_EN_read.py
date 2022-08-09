
import sqlite3
import time
import re
import zlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


conn = sqlite3.connect('index_EN.sqlite')
cur = conn.cursor()

allsenders = list()
cur.execute('''SELECT url,html FROM Pages''')

for URL,HTML in cur:
	print(url, HTML)



def neo4j_bolt(svr_id, host):
    from neomodel import config
    config.DATABASE_URL = os.environ.get(
        'NEO4J_BOLT_URL', 'bolt://user:pass@{0}:{1}'.format(host, svr_id))

KG.neo4j_bolt('7687', 'localhost')

def nrg_cypher(list, func, opr='=~'):

    txt = "MATCH (n:Sim) WHERE n.sim_name {0} $name RETURN ".format(opr)
    for f in func:
        for item in list:
            txt += ("{0}(n.sim_{1}),".format(f, item))
    return(txt[:-1])
