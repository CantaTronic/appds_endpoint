
import db

s = db.sqlalchemy.select([db.event.c.uuid])
s = s.where(db.event.c.ts <= '1998-05-08 16:35:45')
result = db.conn.execute(s)
uuids = []
for row in result:
    uuids.append(row[0])
print(uuids)
