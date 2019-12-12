
import json
import sys

def read_config(config_file_name):
    try:
        config_file = open(config_file_name, "r")
        conf = json.loads(config_file.read())
    except Exception:
        print('Cannot read config file %s' % config_file_name, file=sys.stderr)
        conf = ''
    else:
        config_file.close()
    return conf

def URL(cfg):
    try:
        url = cfg['type'] + '://' \
            + cfg['username'] + ':' \
            + cfg['password'] + '@' \
            + cfg['server'] + ':' \
            + cfg['port'] + '/' \
            + cfg['database']
    except Exception:
        print('Wrong config format %s' % config_file_name, file=sys.stderr)
        url = ''
    return url
