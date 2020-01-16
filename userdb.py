
import sqlalchemy
import pathlib

engine = sqlalchemy.create_engine('sqlite:///'+str(pathlib.Path().absolute())+'/user.db')
conn = engine.connect()
MD = sqlalchemy.MetaData()
user = sqlalchemy.Table('user', MD, autoload=True, autoload_with=engine)
request = sqlalchemy.Table('request', MD, autoload=True, autoload_with=engine)
