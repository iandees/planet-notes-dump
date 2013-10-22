from lxml import etree
import psycopg2
import argparse

parser = argparse.ArgumentParser(description='Exports OSM Notes from the database en masse.')
parser.add_argument('output_file', help='File to write the resulting XML to.')
parser.add_argument('--database', help='Postgres database to read from.', default='openstreetmap')
parser.add_argument('--host', help='Postgres hostname to connect to.', default='localhost')
parser.add_argument('--port', help='Postgres port to connect to.', default=5432)
parser.add_argument('--user', help='Postgres username to use when connecting to the database.', default='openstreetmap')
parser.add_argument('--password', help='Postgres password to use when connecting to the database.', default='openstreetmap')
parser.add_argument('--since', help='A datetime to retrieve notes since. Allows incremental dumps.', default='2000-01-01 00:00:00Z')

args = parser.parse_args()

outfile = file(args.output_file, 'w')
outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
outfile.write('<osm version="0.6" generator="planet-notes-dump">\n')

conn = psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password, database=args.database)
note_cursor = conn.cursor()
comment_cursor = conn.cursor()

note_cursor.execute("SELECT id,latitude,longitude,created_at,status,closed_at FROM notes WHERE status != 'hidden' AND updated_at > %s", [args.since])
for note in note_cursor:
    note_elem = etree.Element("note", {'id': str(note[0]),
                                       'lat': '%0.7f' % (note[1] / 10000000.),
                                       'lon': '%0.7f' % (note[2] / 10000000.),
                                       'status': note[4],
                                       'date_created': note[3].replace(microsecond=0).isoformat() + 'Z'})

    if note[4] == 'closed':
        note_elem.attrib['date_closed'] = note[5].replace(microsecond=0).isoformat() + 'Z'

    comment_cursor.execute("SELECT created_at,author_id,users.display_name,body,event FROM note_comments JOIN users ON (note_comments.author_id=users.id) WHERE note_id = %s", [note[0]])
    for comment in comment_cursor:
        comment_elem = etree.SubElement(note_elem, "comment", {'date': comment[0].replace(microsecond=0).isoformat() + 'Z',
                                                               'uid': str(comment[1]),
                                                               'user': comment[2],
                                                               'action': comment[4]})
        comment_elem.text = unicode(comment[3], 'utf8')
        
    outfile.write(etree.tostring(note_elem, encoding='utf8', pretty_print=True))

conn.close()

outfile.write('</osm>\n')
outfile.close()
