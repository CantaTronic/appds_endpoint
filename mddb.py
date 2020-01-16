
import sqlalchemy
from read_config import read_config, URL

cfg = read_config('mddb.cfg.json')
engine = sqlalchemy.create_engine(URL(cfg))
conn = engine.connect()
MD = sqlalchemy.MetaData()
event = sqlalchemy.Table('event', MD, autoload=True, autoload_with=engine)
