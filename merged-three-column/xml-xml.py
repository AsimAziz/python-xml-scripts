import xml.etree.ElementTree as ET
import csv
import sys
import xml.dom.minidom
# from bs4 import BeautifulSoup
import urllib
import psycopg2
reload(sys)
sys.setdefaultencoding('utf8')

# file = urllib.urlopen("/var/www/html/xml-python-script/merged-three-column/People_People_aas233_20-Feb-2019-12-17-06.xml")
# soupPep = BeautifulSoup(file,'lxml')

#read from source file 
treeAbs = ET.parse('Abstracts_Abstracts_aas233_20-Feb-2019-12-13-06.xml')
rootAbs = treeAbs.getroot()

# treeSes = ET.parse('Sessions_Sessions_aas233_20-Feb-2019-12-15-09.xml')
# rootSes = treeSes.getroot()

# #read session name from source file 
# session_name = rootSes.find('PROGRAMS')[0].find('NAME').text
# program_name = filter(str.isalpha, session_name)
# program_id = filter(str.isdigit, session_name)

# # #open csv file for write 
# # session_data = open(session_name+'-Session.csv', 'w')
# # csv_session_writer = csv.writer(session_data)

# # #write first row in csv file
# # csv_session_writer.writerow(['SessionID', 'SessionNumber', 'SessionTitle', 'SessionType', 'SessionDay', 'SessionTime', 'SessionLocation', 'PresentationID', 'PresentationNumber', 'PresentationTitle', 'AuthorBlock', 'AbstractBibCode', 'AbstractBody'])

# #open xml file for write
# file_obj = open(session_name+'-Session-Presentation.xml', 'w')


# #function that generate bib code
# def gen_bib_code(data):
#     author_lst_name = data[0].find('LNAME').text
#     author_lst_name_bib = author_lst_name[0]

#     return data[1]+data[2]+'...'+data[3]+data[4]+author_lst_name_bib


# #function that generate author name
# def author_name(author):
#     f_name = author.find('FNAME').text
#     if author.find('MNAME').text is not None:
#         m_name = ' '+author.find('MNAME').text+' '
#     else:
#         m_name = ' '
#     l_name = author.find('LNAME').text

#     return f_name+m_name+l_name

# #function that generate author block
# def gen_author_block(authorsData):
#     author_names_dic = {}
#     author_inst_dic = {}

#     for single_author in authorsData:
        
#         author_inst = single_author.find('AFFILIATIONS')[0].find('INST').text
#         author_number = single_author.find('AFFILIATIONS')[0].get('number')
#         author_n = author_name(single_author) 
#         author_names_dic[author_n] = author_number
#         author_inst_dic[author_number] = author_inst
        
#         author_str = '<div>'
#         author_inst_str = '<div>'
#         for index, (key, value) in enumerate(author_names_dic.iteritems()):
#             if index == 0:
#                 author_str += '<span><em>'+key+'<sup>'+value+'</sup></em></span>'
#             else:
#                 author_str += ', <span>'+key+'<sup>'+value+'</sup></span>'
#         author_str += '</div>'
        
#         for index, (key, value) in enumerate(author_inst_dic.iteritems()):
#             if index == 0:
#                 author_inst_str += key+'. '+value
#             else:
#                 author_inst_str += ', '+key+'. '+value
#         author_inst_str += '</div>'

#     return author_str+author_inst_str   

# #make abstract element for xml file
conn = psycopg2.connect(host='localhost', dbname="xmldata", user="postgres", password="postgres")
cur = conn.cursor()

sql = """SELECT data from persons
            where person_id={0};"""

rootW = ET.Element("ABSTRACTS")


#make abstract childs for xml file
for abstrsct in treeAbs.find('ABSTRACTS'):
    uniqueID = abstrsct.get('id')
    STATUS = abstrsct.find('STATUS').text
    DECISION_STATUS = abstrsct.find('DECISION_STATUS').text
    DECISION_HISTORY = abstrsct.find('DECISION_HISTORY').text
    TITLE = abstrsct.find('TITLE').text
    PRESENTATION_TYPE = abstrsct.find('PRESENTATION_TYPE').text
    SUBMISSION_ROLE = abstrsct.find('SUBMISSION_ROLE')
    ABSTRACT_CATEGORY = abstrsct.find('ABSTRACT_CATEGORY')
    CONTACT_AUTHOR = abstrsct.find('CONTACT_AUTHOR')
    BODY = abstrsct.find('BODY')
    ABSTRACT_DISCLOSURES = abstrsct.find('ABSTRACT_DISCLOSURES')
    ABSTRACT_DETAILS = abstrsct.find('ABSTRACT_DETAILS')
    SYSTEM_TAGS = abstrsct.find('SYSTEM_TAGS')
    CUSTOM_FIELD_1 = abstrsct.find('CUSTOM_FIELD_1').text

    # PRESENTATION_TYPE = TITLE = Session.find('TITLE').text
    # if Session.find('PRESENTATIONS') is not None:
    #     for presentation in  Session.find('PRESENTATIONS'):

    #         inputTag = soupAbs.findAll(attrs={"id" : "3052318"})
    #         print inputTag

    sessionDetails = ET.SubElement(rootW, "ABSTRACT", id=uniqueID)

    if STATUS is not None:
        ET.SubElement(sessionDetails, "STATUS").text = STATUS
    else:
        ET.SubElement(sessionDetails, "STATUS").text = ""

    if DECISION_STATUS is not None:
        ET.SubElement(sessionDetails, "DECISION_STATUS").text = DECISION_STATUS
    else:
        ET.SubElement(sessionDetails, "DECISION_STATUS").text = ""
    
    if DECISION_HISTORY is not None:
        ET.SubElement(sessionDetails, "DECISION_HISTORY").text = DECISION_HISTORY
    else:
        ET.SubElement(sessionDetails, "DECISION_HISTORY").text = ""

    if TITLE is not None:
        ET.SubElement(sessionDetails, "TITLE").text = TITLE
    else:
        ET.SubElement(sessionDetails, "TITLE").text = ""

    if PRESENTATION_TYPE is not None:
        ET.SubElement(sessionDetails, "PRESENTATION_TYPE").text = PRESENTATION_TYPE
    else:
        ET.SubElement(sessionDetails, "PRESENTATION_TYPE").text = ""
    
    SUBMISSIONROLE = ''.join(ET.tostring(e, method='html') for e in SUBMISSION_ROLE)
    ET.SubElement(sessionDetails, "SUBMISSION_ROLE").text = SUBMISSIONROLE
    
    CONTACTAUTHOR = ''.join(ET.tostring(e, method='html') for e in CONTACT_AUTHOR)
    ET.SubElement(sessionDetails, "CONTACT_AUTHOR").text = CONTACTAUTHOR
    
    authorsTag = ET.SubElement(sessionDetails, 'AUTHORS')
    if abstrsct.find('AUTHORS') is not None:
        for author in  abstrsct.find('AUTHORS'):
            person_id = author.get('person_id')
            order = author.get('order')
            presenter = author.get('presenter')
            
            cur.execute(sql.format(int(person_id)))
            row = cur.fetchone()
            if row is not None:
                ET.SubElement(authorsTag, "AUTHOR", person_id=person_id ,order=order, presenter=presenter).text = row[0]
            else:
                AUTHORDATAs = ''.join(ET.tostring(e, method='html') for e in author)
                ET.SubElement(authorsTag, "AUTHOR", person_id=person_id ,order=order, presenter=presenter).text = AUTHORDATAs

    if BODY is not None:
        BODYDATA = ''.join(ET.tostring(e, method='html') for e in BODY)
        ET.SubElement(sessionDetails, "BODY").text = BODYDATA

    if ABSTRACT_DISCLOSURES is not None:
        ABSTRACTDISCLOSURES = ''.join(ET.tostring(e, method='html') for e in ABSTRACT_DISCLOSURES)
        ET.SubElement(sessionDetails, "ABSTRACT_DISCLOSURES").text = ABSTRACTDISCLOSURES
    
    if ABSTRACT_DETAILS is not None:
        ABSTRACTDETAILS = ''.join(ET.tostring(e, method='html') for e in ABSTRACT_DETAILS)
        ET.SubElement(sessionDetails, "ABSTRACT_DETAILS").text = ABSTRACTDETAILS

    if ABSTRACT_CATEGORY is not None:
        ABSTRACTCATEGORY = ''.join(ET.tostring(e, method='html') for e in ABSTRACT_CATEGORY)
        ET.SubElement(sessionDetails, "ABSTRACT_CATEGORY").text = ABSTRACTCATEGORY
    
    if SYSTEM_TAGS is not None:
        SYSTEMTAGS = ''.join(ET.tostring(e, method='html') for e in SYSTEM_TAGS)
        ET.SubElement(sessionDetails, "SYSTEM_TAGS").text = SYSTEMTAGS

    if CUSTOM_FIELD_1 is not None:
        ET.SubElement(sessionDetails, "CUSTOM_FIELD_1").text = CUSTOM_FIELD_1
    else:
        ET.SubElement(sessionDetails, "CUSTOM_FIELD_1").text = ""

file_obj = open('AbstractAuthor.xml', 'w')
xml_data =  ET.tostring(rootW, encoding='UTF-8', method='xml')

#write encoded xml data in xml file 
file_obj.write(xml_data)

#close xml file
file_obj.close
