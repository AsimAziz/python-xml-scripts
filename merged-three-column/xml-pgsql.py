import xml.etree.ElementTree as ET
import csv
import sys
import xml.dom.minidom
from bs4 import BeautifulSoup
import urllib
import psycopg2
reload(sys)
sys.setdefaultencoding('utf8')

conn = psycopg2.connect(host='localhost', dbname="xmldata", user="postgres", password="postgres")
cur = conn.cursor()

sql = """INSERT INTO abstracts(abstract_id,data)
            VALUES(%s, %s);"""

treeAbs = ET.parse('AbstractAuthor.xml')
rootAbs = treeAbs.getroot()

# for person in treeAbs.find('ABSTRACTS'):
#     uniqueID = person.get('id')
#     individual_person = ''

#     for person_child in person._children:
#         individual_person +=  ET.tostring(person_child, method='html')

for abstract in rootAbs._children:
    uniqueID = abstract.get('id')
    individual_abstract = ''

    for person_child in abstract._children:
        individual_abstract +=  ET.tostring(person_child, method='html')

    cur.execute(sql,(uniqueID, individual_abstract))
    conn.commit()
    print "individual_abstract"