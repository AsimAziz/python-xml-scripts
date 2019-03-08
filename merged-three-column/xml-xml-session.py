import xml.etree.ElementTree as ET
import csv
import sys
import xml.dom.minidom
# from bs4 import BeautifulSoup
import urllib
import psycopg2
reload(sys)
sys.setdefaultencoding('utf8')


#read from source file 
treeAbs = ET.parse('Sessions_Sessions_aas233_20-Feb-2019-12-15-09.xml')
rootAbs = treeAbs.getroot()

conn = psycopg2.connect(host='localhost', dbname="xmldata", user="postgres", password="postgres")
cur = conn.cursor()

sql = """SELECT data from abstracts
            where abstract_id={0};"""

rootW = ET.Element("SESSIONS")


#make abstract childs for xml file
for abstrsct in treeAbs.find('SESSIONS'):
    sess_id = abstrsct.get('sess_id')
    itin_level_id = abstrsct.get('itin_level_id')
    parent_itin_level_id = abstrsct.get('parent_itin_level_id')
    program_id = abstrsct.get('program_id')
    csid = abstrsct.get('csid')
    kind = abstrsct.get('kind')
    in_ip = abstrsct.get('in_ip')
    is_invited = abstrsct.get('is_invited')
    is_ticketed = abstrsct.get('is_ticketed')
    show_abstract_times = abstrsct.get('show_abstract_times')
    session_status = abstrsct.get('session_status')

    sessionDetails = ET.SubElement(rootW, "SESSION", sess_id=sess_id, itin_level_id=itin_level_id, parent_itin_level_id=parent_itin_level_id, program_id=program_id, csid=csid, kind=kind, in_ip=in_ip, is_invited=is_invited, is_ticketed=is_ticketed, show_abstract_times=show_abstract_times, session_status=session_status)

    LEVEL_NAME = abstrsct.find('LEVEL_NAME').text
    ET.SubElement(sessionDetails, "LEVEL_NAME").text = LEVEL_NAME

    SESSION_TITLE = abstrsct.find('SESSION_TITLE').text
    ET.SubElement(sessionDetails, "SESSION_TITLE").text = SESSION_TITLE

    SESSION_ABBR = abstrsct.find('SESSION_ABBR').text
    ET.SubElement(sessionDetails, "SESSION_ABBR").text = SESSION_ABBR

    SESSION_TYPE = abstrsct.find('SESSION_TYPE').text
    ET.SubElement(sessionDetails, "SESSION_TYPE").text = SESSION_TYPE

    SESSION_TRACK = abstrsct.find('SESSION_TRACK').text
    ET.SubElement(sessionDetails, "SESSION_TRACK").text = SESSION_TRACK

    SYMPOSIA_NAME = abstrsct.find('SYMPOSIA_NAME').text
    ET.SubElement(sessionDetails, "SYMPOSIA_NAME").text = SYMPOSIA_NAME

    SESSION_NOTES = abstrsct.find('SESSION_NOTES').text
    ET.SubElement(sessionDetails, "SESSION_NOTES").text = SESSION_NOTES

    SESSION_NOTES_ADMIN = abstrsct.find('SESSION_NOTES_ADMIN').text
    ET.SubElement(sessionDetails, "SESSION_NOTES_ADMIN").text = SESSION_NOTES_ADMIN

    SESSION_SPONSOR = abstrsct.find('SESSION_SPONSOR').text
    ET.SubElement(sessionDetails, "SESSION_SPONSOR").text = SESSION_SPONSOR

    SESSION_EXPECTED_ATTENDANCE = abstrsct.find('SESSION_EXPECTED_ATTENDANCE').text
    ET.SubElement(sessionDetails, "SESSION_EXPECTED_ATTENDANCE").text = SESSION_EXPECTED_ATTENDANCE

    SESSION_ACTUAL_ATTENDANCE = abstrsct.find('SESSION_ACTUAL_ATTENDANCE').text
    ET.SubElement(sessionDetails, "SESSION_ACTUAL_ATTENDANCE").text = SESSION_ACTUAL_ATTENDANCE

    SESSION_LEARNING_OBJ_01 = abstrsct.find('SESSION_LEARNING_OBJ_01').text
    ET.SubElement(sessionDetails, "SESSION_LEARNING_OBJ_01").text = SESSION_LEARNING_OBJ_01

    SESSION_LEARNING_OBJ_02 = abstrsct.find('SESSION_LEARNING_OBJ_02').text
    ET.SubElement(sessionDetails, "SESSION_LEARNING_OBJ_02").text = SESSION_LEARNING_OBJ_02

    SESSION_LEARNING_OBJ_03 = abstrsct.find('SESSION_LEARNING_OBJ_03').text
    ET.SubElement(sessionDetails, "SESSION_LEARNING_OBJ_03").text = SESSION_LEARNING_OBJ_03
    

    SESSION_DATE = abstrsct.find('SESSION_DATE')
    if SESSION_DATE is not None:
        SESSIONDATE = ''.join(ET.tostring(e, method='html') for e in SESSION_DATE)
        ET.SubElement(sessionDetails, "SESSION_DATE").text = SESSIONDATE
    
    SESSION_START_TIME = abstrsct.find('SESSION_START_TIME')
    if SESSION_START_TIME is not None:
        SESSIONSTARTTIME = ''.join(ET.tostring(e, method='html') for e in SESSION_START_TIME)
        ET.SubElement(sessionDetails, "SESSION_START_TIME").text = SESSIONSTARTTIME    
    
    SESSION_END_TIME = abstrsct.find('SESSION_END_TIME')
    if SESSION_END_TIME is not None:
        SESSIONENDTIME = ''.join(ET.tostring(e, method='html') for e in SESSION_END_TIME)
        ET.SubElement(sessionDetails, "SESSION_END_TIME").text = SESSIONENDTIME 
    
    SESSION_CREATOR = abstrsct.find('SESSION_CREATOR')
    if SESSION_CREATOR is not None:
        person_id = SESSION_CREATOR.get('person_id')
        SESSIONCREATOR = ''.join(ET.tostring(e, method='html') for e in SESSION_CREATOR)
        ET.SubElement(sessionDetails, "SESSION_CREATOR", person_id=person_id).text = SESSIONCREATOR 

    SESSION_DURATION_MINUTES = abstrsct.find('SESSION_DURATION_MINUTES').text
    ET.SubElement(sessionDetails, "SESSION_DURATION_MINUTES").text = SESSION_DURATION_MINUTES

    SESSION_LOCATION = abstrsct.find('SESSION_LOCATION')
    if SESSION_LOCATION is not None:
        SESSIONLOCATION = ''.join(ET.tostring(e, method='html') for e in SESSION_LOCATION)
        ET.SubElement(sessionDetails, "SESSION_LOCATION").text = SESSIONLOCATION 

    SESSION_OWNERS = abstrsct.find('SESSION_OWNERS')
    if SESSION_OWNERS is not None:
        SESSIONOWNERS = ''.join(ET.tostring(e, method='html') for e in SESSION_OWNERS)
        ET.SubElement(sessionDetails, "SESSION_OWNERS").text = SESSIONOWNERS    
   
    SESSION_HOSTS = abstrsct.find('SESSION_HOSTS')
    if SESSION_HOSTS is not None:
        SESSIONHOSTS = ''.join(ET.tostring(e, encoding='UTF-8', method='xml') for e in SESSION_HOSTS)
        ET.SubElement(sessionDetails, "SESSION_HOSTS").text = SESSIONHOSTS 

    
    presentationTag = ET.SubElement(sessionDetails, 'PRESENTATIONS')
    if abstrsct.find('PRESENTATIONS') is not None:
        for presentaion in  abstrsct.find('PRESENTATIONS'):
            id = presentaion.get('id')
            sess_sort = presentaion.get('sess_sort')
            control_id = presentaion.get('control_id')
            type = presentaion.get('type')

            cur.execute(sql.format(int(control_id)))
            row = cur.fetchone()
            if row is not None:
                ET.SubElement(presentationTag, "PRESENTATION", id=id ,sess_sort=sess_sort, control_id=control_id, type=type).text = row[0]
            else:
                presentaionDATAs = ''.join(ET.tostring(e, method='html') for e in presentaion)
                ET.SubElement(presentationTag, "PRESENTATION", id=id ,sess_sort=sess_sort, control_id=control_id, type=type).text = presentaionDATAs



    # if ABSTRACT_DISCLOSURES is not None:
    #     ABSTRACTDISCLOSURES = ''.join(ET.tostring(e, method='html') for e in ABSTRACT_DISCLOSURES)
    #     ET.SubElement(sessionDetails, "ABSTRACT_DISCLOSURES").text = ABSTRACTDISCLOSURES
    
    # if ABSTRACT_DETAILS is not None:
    #     ABSTRACTDETAILS = ''.join(ET.tostring(e, method='html') for e in ABSTRACT_DETAILS)
    #     ET.SubElement(sessionDetails, "ABSTRACT_DETAILS").text = ABSTRACTDETAILS

    # if ABSTRACT_CATEGORY is not None:
    #     ABSTRACTCATEGORY = ''.join(ET.tostring(e, method='html') for e in ABSTRACT_CATEGORY)
    #     ET.SubElement(sessionDetails, "ABSTRACT_CATEGORY").text = ABSTRACTCATEGORY
    
    # if SYSTEM_TAGS is not None:
    #     SYSTEMTAGS = ''.join(ET.tostring(e, method='html') for e in SYSTEM_TAGS)
    #     ET.SubElement(sessionDetails, "SYSTEM_TAGS").text = SYSTEMTAGS

    # if CUSTOM_FIELD_1 is not None:
    #     ET.SubElement(sessionDetails, "CUSTOM_FIELD_1").text = CUSTOM_FIELD_1
    # else:
    #     ET.SubElement(sessionDetails, "CUSTOM_FIELD_1").text = ""

    file_obj = open('SessionAbstractAuthor.xml', 'w')
    xml_data =  ET.tostring(rootW, encoding='UTF-8', method='xml')

#write encoded xml data in xml file 
    file_obj.write(xml_data)

#close xml file
file_obj.close
