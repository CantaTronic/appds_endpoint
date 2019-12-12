
import pymongo
import sqlalchemy
from read_config import URL

if __name__ == '__main__':
    cfg_mongo = read_config('kcdc.cfg.json')
    client = pymongo.MongoClient(URL(cfg_mongo))
    db = client[cfg['database']]
    data = db['data']
    cur = data.find( { 'general.Gt': { '$gte': 1078741512, '$lte': 1078741599 } } )

    cfg_sql = read_config('mddb.cfg.json')
    engine = sqlalchemy.create_engine(URL(cfg_sql))
    conn = engine.connect()
    MD = sqlalchemy.MetaData()
    event = sqlalchemy.Table('event', MD, autoload=True, autoload_with=engine)
    kascade_exp = sqlalchemy.Table('kascade_exp', MD, autoload=True, autoload_with=engine)
    kascade_cond = sqlalchemy.Table('kascade_cond', MD, autoload=True, autoload_with=engine)

    i = 0
    p_ts = 0
    p_temp = -274.
    p_press = -1.
    for ev in cur:
        i += 1
        print(i, ev['general']['UUID'])
        ins = event.insert().values(
            id       = i,
            uuid     = ev['general']['UUID'],
            type     = 0,
            storage  = 0,
            version  = 3,
            location = 0,
            ts       = ev['general']['Gt'],
            ns       = ev['general']['M'],
            energy   = ev['array']['E'],
            zenith   = ev['array']['Ze'],
            azimuth  = ev['array']['Az']
        )
        conn.execute(ins)
        ins = kascade_exp.insert().values(
            id              = i,
            core_x          = ev['array']['Xc'],
            core_y          = ev['array']['Yc'],
            electron_number = ev['array']['Ne'],
            muon_number     = ev['array']['Nmu'],
            shower_age      = ev['array']['Age']
        )
        conn.execute(ins)
        if ev['general']['Gt'] > p_ts \
        and p_temp != ev['general']['T'] \
        and p_press != ev['general']['P']:
            p_ts = ev['general']['Gt']
            p_temp = ev['general']['T']
            p_press = ev['general']['P']
            ins = kascade_cond.insert().values(
                ts          = ev['general']['Gt'],
                temperature = ev['general']['T'],
                pressure    = ev['general']['P']
            )
            conn.execute(ins)
