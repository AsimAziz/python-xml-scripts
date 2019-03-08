import xml.etree.ElementTree as ET
import csv
import sys
import xml.dom.minidom
reload(sys)
sys.setdefaultencoding('utf8')

#read from source file 
tree = ET.parse('AAS233_Sessions_1221_Sessions_aas233_21-Dec-2018-00-18-09.xml')
root = tree.getroot()

#read session name from source file 
session_name = root.find('PROGRAMS')[0].find('NAME').text
program_name = filter(str.isalpha, session_name)
program_id = filter(str.isdigit, session_name)

#open csv file for write 
session_data = open(session_name+'-Session.csv', 'w')
csv_session_writer = csv.writer(session_data)

#write first row in csv file
csv_session_writer.writerow(['SessionID', 'SessionNumber', 'SessionTitle', 'SessionType', 'SessionDay', 'SessionTime', 'SessionLocation', 'PresentationID', 'PresentationNumber', 'PresentationTitle', 'AuthorBlock', 'AbstractBibCode', 'AbstractBody'])

#open xml file for write
file_obj = open(session_name+'-Session.xml', 'w')


#function that generate bib code
def gen_bib_code(data):
    author_lst_name = data[0].find('LNAME').text
    author_lst_name_bib = author_lst_name[0]

    return data[1]+data[2]+'...'+data[3]+data[4]+author_lst_name_bib


#function that generate author name
def author_name(author):
    f_name = author.find('FNAME').text
    if author.find('MNAME').text is not None:
        m_name = ' '+author.find('MNAME').text+' '
    else:
        m_name = ' '
    l_name = author.find('LNAME').text

    return f_name+m_name+l_name

#function that generate author block
def gen_author_block(authorsData):
    author_names_dic = {}
    author_inst_dic = {}

    for single_author in authorsData:
        
        author_inst = single_author.find('AFFILIATIONS')[0].find('INST').text
        author_number = single_author.find('AFFILIATIONS')[0].get('number')
        author_n = author_name(single_author) 
        author_names_dic[author_n] = author_number
        author_inst_dic[author_number] = author_inst
        
        author_str = '<div>'
        author_inst_str = '<div>'
        for index, (key, value) in enumerate(author_names_dic.iteritems()):
            if index == 0:
                author_str += '<span><em>'+key+'<sup>'+value+'</sup></em></span>'
            else:
                author_str += ', <span>'+key+'<sup>'+value+'</sup></span>'
        author_str += '</div>'
        
        for index, (key, value) in enumerate(author_inst_dic.iteritems()):
            if index == 0:
                author_inst_str += key+'. '+value
            else:
                author_inst_str += ', '+key+'. '+value
        author_inst_str += '</div>'

    return author_str+author_inst_str   

#make abstract element for xml file
rootW = ET.Element("AbstractBook", meetingID=program_id+"nd Meeting of the American Astronomical Society")

#make abstract childs for xml file
for Session in root.find('SESSIONS'):
    uniqueID = Session.get('sess_id')
    SessionTitle = Session.find('SESSION_TITLE').text
    SessionType = Session.find('SESSION_TYPE').text
    sessionDay = Session.find('SESSION_DATE').find('DAY_NAME').text
    sessionYear = Session.find('SESSION_DATE').find('YEAR').text
    
    session_start_t = Session.find('SESSION_START_TIME')
    session_start_time = session_start_t.find('HOUR').text+':'+session_start_t.find('MINUTE').text+' '+session_start_t.find('AM_PM').text

    session_end_t = Session.find('SESSION_END_TIME')
    session_end_time = session_end_t.find('HOUR').text+':'+session_end_t.find('MINUTE').text+' '+session_end_t.find('AM_PM').text
    
    SessionTime = session_start_time+'-'+session_end_time
    SessionLocation = Session.find('SESSION_LOCATION').find('VENUE').text
    
    if Session.find('PRESENTATIONS') is not None:
        sess_num = Session.find('PRESENTATIONS')[0]
        if sess_num.find('FINAL_ID').text is not None:
            session_num = sess_num.find('FINAL_ID').text.split('.')
            SessionNumber = session_num[0]
        else:
            SessionNumber = ''

    sessionDetails = ET.SubElement(rootW, "SessionDetail", uniqueID=uniqueID)
    ET.SubElement(sessionDetails, "SessionNumber").text = SessionNumber
    ET.SubElement(sessionDetails, "SessionTitle").text = SessionTitle
    ET.SubElement(sessionDetails, "SessionTypeName").text = SessionType
    ET.SubElement(sessionDetails, "SessionDay").text = sessionDay
    ET.SubElement(sessionDetails, "SessionTime").text = SessionTime
    ET.SubElement(sessionDetails, "SessionLocation").text = SessionLocation
    presentations = ET.SubElement(sessionDetails, "Presentations")

#make abstract->presentation childs for xml file
    if Session.find('PRESENTATIONS') is not None:
        for present in Session.find('PRESENTATIONS'):

            pre_uniqueID = present.get('id')
            pre_title = present.find('TITLE').text

            if present.find('FINAL_ID').text is not None:
                PresentationNumber = present.find('FINAL_ID').text
                final_id_bib = PresentationNumber.replace(".","")
            else:
                PresentationNumber = ''
                final_id_bib = ''
            
            if present.find('BODY') is not None:
                AbstractBody = present.find('BODY')[0].find('TEXT').text
            else:
                AbstractBody = ''
            
            #making author block and bibcode
            if present.find('AUTHORS') is not None:
                single_author = present.find('AUTHORS')[0]
                all_authors_data = present.find('AUTHORS')
                bib_code_data_array = [single_author, sessionYear, program_name, program_id, final_id_bib]

                bib_code = gen_bib_code(bib_code_data_array)
                AuthorBlock = gen_author_block(all_authors_data)
                
            else:
                AuthorBlock = ''
                bib_code = ''

            presentation = ET.SubElement(presentations, "Presentation", uniqueID=pre_uniqueID)
            ET.SubElement(presentation, "PresentationNumber").text = PresentationNumber
            ET.SubElement(presentation, "PresentationTitle").text = pre_title
            ET.SubElement(presentation, "AuthorBlock").text = AuthorBlock
            ET.SubElement(presentation, "AbstractBibCode").text = bib_code
            ET.SubElement(presentation, "AbstractBody").text = AbstractBody

            csv_session_writer.writerow([uniqueID, SessionNumber, SessionTitle, SessionType, sessionDay, SessionTime, SessionLocation, pre_uniqueID, PresentationNumber, pre_title, AuthorBlock, bib_code, AbstractBody])

#encode xml elements and their child 
xml_data =  ET.tostring(rootW, encoding='UTF-8', method='xml')

#write encoded xml data in xml file 
file_obj.write(xml_data)

#close xml file
file_obj.close
