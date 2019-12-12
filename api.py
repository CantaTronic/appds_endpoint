
import flask
import mddb
import kcdc
import txtwriter
import hashlib
import uuid
import sys
from read_config import read_config

app = flask.Flask(__name__)
app.config['DEBUG'] = True

try:
    salt = read_config('salt.json')['salt']
except Exception:
    print('Cannot load password salt', file=sys.stderr)
    exit(1)

@app.route('/', methods=['GET'])
def home():
    return '<h1>Test</h1><p>Test test test.</p>'

@app.route('/api/doc/', methods=['GET'])
def api_doc():
    return app.send_static_file('doc.html')

@app.route('/api/my_requests/', methods=['POST'])
def api_my_requests():
    content = flask.request.json
    user_id = get_user_id(content)
    sel = mddb.sqlalchemy.select([mddb.request.c.uuid, mddb.request.c.status, mddb.request.c.format])
    sel = sel.where(mddb.request.c.user_id == user_id)
    result = mddb.conn.execute(sel)
    reply = { 'requests': [] }
    for row in result:
        reply['requests'].append(format_req(row))
    return flask.jsonify(reply)

@app.route('/api/request_status/<string:request_uuid>/', methods=['POST'])
def api_request_status(request_uuid):
    content = flask.request.json
    user_id = get_user_id(content)
    sel = mddb.sqlalchemy.select([mddb.request.c.uuid, mddb.request.c.status, mddb.request.c.format])
    sel = sel.where(mddb.request.c.uuid == request_uuid)
    sel = sel.where(mddb.request.c.user_id == user_id)
    res = mddb.conn.execute(sel).fetchone()
    if res is None:
        flask.abort(404, 'No request '+request_uuid)
    return flask.jsonify(format_req(res))

@app.route('/api/data/<string:filename>', methods=['POST'])
def api_download(filename):
    content = flask.request.json
    user_id = get_user_id(content)
    flask.abort(501, 'Not implemented yet')
    # TODO download a file

@app.route('/api/request/', methods=['POST'])
def api_request():
    content = flask.request.json
    user_id = get_user_id(content)
    if not 'format' in content:
        flask.abort(400, 'No \'format\' provided')
    fmt = content['format'].upper()
    if fmt != 'ASCII' and fmt != 'ROOT' and fmt != 'HDF5':
        flask.abort(401, 'Invalid \'format\'')
    request_uuid = str(uuid.uuid4())
    ins = mddb.request.insert().values(
        uuid=request_uuid,
        user_id=user_id,
        format=fmt,
        status=1
    )
    mddb.conn.execute(ins)
    # TODO check UUID collisions
    reply = {}
    reply['request_id'] = request_uuid
    #reply['format'] = fmt
    #reply['num_events'] = nev
    #reply['event_uuids'] = uuids
    reply['file_url'] = 'api/data/'+request_uuid
    if fmt == 'ASCII':
        reply['file_url'] += '.txt'
    elif fmt == 'ROOT':
        reply['file_url'] += '.root'
    elif fmt == 'HDF5':
        reply['file_url'] += '.hdf5'
    return flask.jsonify(reply)
    # TODO: start async task
    #sel = mddb.sqlalchemy.select([mddb.event.c.uuid])
    #if 'start_time' in content:
        #sel = sel.where(mddb.event.c.ts >= content['start_time'])
    #if 'end_time' in content:
        #sel = sel.where(mddb.event.c.ts < content['end_time'])
    #result = mddb.conn.execute(sel)
    ##uuids = []
    #nev = 0
    #fout = txtwriter.TxtWriter('tmp.txt')
    #for row in result:
        #uuid = row[0]
        ##uuids.append(uuid)
        #nev += 1
        #evt = kcdc.data.find_one( {'general.UUID': uuid} )
        #fout.write(evt)

def get_user_id(j):
    if not 'username' in j:
        flask.abort(400, 'No \'username\' provided')
    if not 'password' in j:
        flask.abort(400, 'No \'password\' provided')
    sel = mddb.sqlalchemy.select([mddb.user.c.id])
    sel = sel.where(mddb.user.c.name == j['username'])
    sel = sel.where(mddb.user.c.pass_sha1 == hashlib.sha1((j['password']+salt).encode()).hexdigest())
    res = mddb.conn.execute(sel).fetchone()
    if res is None:
        flask.abort(401, 'Cannot authenticate, invalid username or password')
    return int(res[mddb.user.c.id])

def format_req(row):
    req = { 'uuid': row['uuid'] }
    status = row['status']
    if status == 1:
        status = 'processing'
    elif status == 2:
        status = 'completed'
    elif status == 3:
        status = 'failed'
    req['status'] = status
    fmt = row['format']
    req['file_url'] = 'api/data/'+row['uuid']
    if fmt == 'ASCII':
        req['file_url'] += '.txt'
    elif fmt == 'ROOT':
        req['file_url'] += '.root'
    elif fmt == 'HDF5':
        req['file_url'] += '.hdf5'
    return req

if __name__ == '__main__':
    app.run()
