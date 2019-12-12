
import pymongo
from read_config import read_config, URL

cfg = read_config('kcdc.cfg.json')
client = pymongo.MongoClient(URL(cfg))
db = client[cfg['database']]
data = db['data']
