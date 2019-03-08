

import urllib
import csv
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')


session_data = open('sessionData.csv', 'w')
csv_session_writer = csv.writer(session_data)
csv_session_writer.writerow(['SESSION DATE TIME', 'SESSION TIME', 'SESSION ROOM', 'SESSION TITLE', 'SESSION ABBERIVATION', 'HOSTS', 'FINAL ID', 'PRESENTATION TITLE', 'AUTHOR', 'INSTITUTION', 'ABSTRACT BODY'])

file = urllib.urlopen("/var/www/html/xml-python-script/html-excel/Matt_Test_Sessions_aas233_17-Jan-2019-20-08-09.html")
from bs4 import BeautifulSoup
soup = BeautifulSoup(file, 'html.parser')

# print soup
body = soup.findAll("body")
#print body
countr = -1
session_dates = []
session_room = []
session_time = []
pres_author = []
session_abbrivation = []
session_title = []
host_role = []
final_id = []
abstract_title = []
institutions = []
abstract_body = []


for i in soup.body:
    if i != '\n' and i.has_attr("class"):
        if i['class'][0] == 'session_date':
            countr += 1
            if len(final_id) != countr:
                pres_author.append([])
                abstract_title.append([])
                final_id.append([])
                institutions.append([])
                abstract_body.append([])
            if len(host_role) != countr:
                host_role.append([])
            session_date = i.text
            session_dates.append(session_date)

        if i['class'][0] == 'session_time':
            session_time.append(i.text)
        
        if i['class'][0] == 'session_room':
            session_room.append(i.text)

        if i['class'][0] == 'session_label':
            session_label = i.findChildren("span" , recursive=False)
            if len(session_label) == 2:
                session_abbrivation.append(session_label[0].text)
                session_title.append(session_label[1].text)
            else:
                session_abbrivation.append('')
                session_title.append(session_label[0].text)
        
        if i['class'][0] == 'host_role':
            session_host = i.findChildren("span" , recursive=False)
            host_name = session_host[1].text
            host_des = session_host[0].text
            inner_string = host_des+host_name
            if len(host_role) == countr:
                host_role.append(inner_string)
            else:
                host_role[countr] = host_role[countr]+', '+inner_string

        if i['class'][0] == 'abstract_label':
            session_label = i.findChildren("span" , recursive=False)
            if len(session_label) == 2:
                abstract_title_v = session_label[1].text
                final_id_v = session_label[0].text
            else:
                abstract_title_v = session_label[0].text
                final_id_v = ''
            if len(final_id) == countr:
                inner_array_title = [abstract_title_v]
                inner_array_id = [final_id_v]
                final_id.append(inner_array_id)
                abstract_title.append(inner_array_title)

            else:
                final_id[countr].append(final_id_v)
                abstract_title[countr].append(abstract_title_v)

        if i['class'][0] == 'authors':
            actuall = ''
            for val in i.contents:
                if isinstance(val, basestring):
                    actuall += val.string
                else:
                    actuall += '<'+val.string+'>'
            # if len(i.contents) > 1:
            #     name = i.contents[0]
            #     number = i.contents[1].string
            #     number = '<sup>'+number+'<sup>'
            # else:
            #     name = i.contents[0]
            #     number = ''
            # actuall = name+number
            if len(pres_author) == countr:
                inner_array = [actuall]
                pres_author.append(inner_array)
            else:
                pres_author[countr].append(actuall)
            print actuall

        if i['class'][0] == 'institutions':
            actuall = ''
            for val in i.contents:
                if isinstance(val, basestring):
                    actuall += val.string
                else:
                    actuall += '<'+val.string+'>'
            if len(institutions) == countr:
                inner_array_ins = [actuall]
                institutions.append(inner_array_ins)
            else:
                institutions[countr].append(actuall)
        
        if i['class'][0] == 'abstract_body':
            abstract_body_v = i.text
            #abstract_body_v = abstract_body_arr[0].text
            if len(abstract_body) == countr:
                inner_array_abs = [abstract_body_v]
                abstract_body.append(inner_array_abs)
            else:
                abstract_body[countr].append(abstract_body_v)

pres_author.append([])
abstract_title.append([])
final_id.append([])
institutions.append([])
abstract_body.append([])
host_role.append([])

for idx, val in enumerate(session_dates):
    s_date = val
    s_time = session_time[idx]
    s_room = session_room[idx]
    s_title = session_title[idx]
    s_abbrivation = session_abbrivation[idx]
    h_role = host_role[idx]

    if len(final_id[idx]) > 0:
        for index, value in enumerate(final_id[idx]):
            f_id = value
            a_title = abstract_title[idx][index]
            p_author = pres_author[idx][index]
            institus = institutions[idx][index]
            a_body = abstract_body[idx][index]

            csv_session_writer.writerow([s_date, s_time, s_room, s_title, s_abbrivation, h_role, f_id, a_title, p_author, institus, a_body])
    else:
        csv_session_writer.writerow([s_date, s_time, s_room, s_title, s_abbrivation, h_role])
