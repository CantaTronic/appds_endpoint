
import flask
import mddb
import userdb
import kcdc
import txtwriter
import hashlib
import uuid
import os
import sys
from read_config import read_config

app = flask.Flask(__name__)
app.config['DEBUG'] = True

try:
    salt = read_config('salt.json')['salt']
except Exception:
    print('Cannot load password salt', file=sys.stderr)
    exit(1)

formats = { 'ASCII': '.txt', 'ROOT': '.root', 'HDF5': '.hdf5' }

@app.route('/', methods=['GET'])
def home():
    return '<h1>Test</h1><p>Test test test.</p>'

@app.route('/api/doc/', methods=['GET'])
def api_doc():
    return app.send_static_file('doc.html')

@app.route('/api/my_requests/', methods=['POST'])
def api_my_requests():
    req = flask.request.json
    user_id = get_user_id(req)
    sel = userdb.sqlalchemy.select([userdb.request.c.uuid, userdb.request.c.status, userdb.request.c.format])
    sel = sel.where(userdb.request.c.user_id == user_id)
    result = userdb.conn.execute(sel)
    reply = { 'requests': [] }
    for row in result:
        reply['requests'].append(format_req(row))
    return flask.jsonify(reply)

@app.route('/api/request_status/<string:request_uuid>/', methods=['POST'])
def api_request_status(request_uuid):
    req = flask.request.json
    user_id = get_user_id(req)
    sel = userdb.sqlalchemy.select([userdb.request.c.uuid, userdb.request.c.status, userdb.request.c.format])
    sel = sel.where(userdb.request.c.uuid == request_uuid)
    sel = sel.where(userdb.request.c.user_id == user_id)
    res = userdb.conn.execute(sel).fetchone()
    if res is None:
        flask.abort(404, 'No request '+request_uuid)
    return flask.jsonify(format_req(res))

@app.route('/api/data/<string:filename>', methods=['POST'])
def api_download(filename):
    req = flask.request.json
    user_id = get_user_id(req)
    #flask.abort(501, 'Not implemented yet')
    # TODO check whether file exists and belongs to the user
    path = os.path.abspath(os.path.join(os.getcwd(), 'data'))
    return flask.send_from_directory(path, filename)

@app.route('/api/request/', methods=['POST'])
def api_request():
    req = flask.request.json
    user_id = get_user_id(req)
    if not 'format' in req:
        flask.abort(400, 'No \'format\' provided')
    req['format'] = req['format'].upper()
    if req['format'] not in formats:
        flask.abort(400, 'Invalid \'format\'')
    req['uuid'] = str(uuid.uuid4())
    # TODO check UUID collisions
    ins = userdb.request.insert().values(
        uuid=req['uuid'],
        user_id=user_id,
        format=req['format'],
        status='processing'
    )
    userdb.conn.execute(ins)
    # TODO: async start task
    get_data(req)
    reply = {}
    reply['request_uuid'] = req['uuid']
    #reply['num_events'] = nev
    #reply['event_uuids'] = uuids
    reply['file_url'] = 'api/data/'+req['uuid']+formats[req['format']]
    return flask.jsonify(reply)

def get_data(j):
    sel = mddb.sqlalchemy.select([mddb.event.c.uuid])
    if 'start_time' in j:
        sel = sel.where(mddb.event.c.ts >= j['start_time'])
    if 'end_time' in j:
        sel = sel.where(mddb.event.c.ts < j['end_time'])
    result = mddb.conn.execute(sel)
    nev = 0
    fout = txtwriter.TxtWriter('data/'+j['uuid']+formats[j['format']])
    for row in result:
        uuid = row[0]
        nev += 1
        evt = kcdc.data.find_one( {'general.UUID': uuid} )
        fout.write(evt)
    upd = userdb.request.update().values(status='completed')
    upd = upd.where(userdb.request.c.uuid == j['uuid'])
    userdb.conn.execute(upd)

def get_user_id(j):
    if not 'username' in j:
        flask.abort(400, 'No \'username\' provided')
    if not 'password' in j:
        flask.abort(400, 'No \'password\' provided')
    sel = userdb.sqlalchemy.select([userdb.user.c.id])
    sel = sel.where(userdb.user.c.name == j['username'])
    pass_hash = hashlib.sha1((j['username']+j['password']+salt).encode()).hexdigest()
    sel = sel.where(userdb.user.c.pass_sha1 == pass_hash)
    res = userdb.conn.execute(sel).fetchone()
    if res is None:
        flask.abort(401, 'Cannot authenticate, invalid username or password')
    return int(res[userdb.user.c.id])

def format_req(row):
    req = { 'uuid': row['uuid'], 'status': row['status'] }
    req['file_url'] = 'api/data/'+row['uuid']+formats[row['format']]
    return req

if __name__ == '__main__':
    app.run()
