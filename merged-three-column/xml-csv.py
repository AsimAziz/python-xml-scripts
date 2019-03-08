import xml.etree.ElementTree as ET
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

tree = ET.parse('1205SessionTest_Sessions_aas233_05-Dec-2018-11-54-07.xml')
root = tree.getroot()

session_data = open('sessionData.xlsx', 'w')
csv_session_writer = csv.writer(session_data)

presentation_data = open('presentationData.xlsx', 'w')
csv_present_writer = csv.writer(presentation_data)

present_auth_data = open('presentAuthData.xlsx', 'w')
csv_present_auth_writer = csv.writer(present_auth_data)

linking_data = open('linkingData.xlsx', 'w')
csv_linking_writer = csv.writer(linking_data)

csv_session_writer.writerow(['Session ID', 'Session Title', 'Start Date/Time', 'date', 'start', 'End Date/Time', 'end', 'Room/Location',	'Schedule Track','' ,'' , 'Description'])
csv_present_writer.writerow(['Session ID', 'Presentation ID', 'Name', 'Sub-Title', 'Description', 'Room/Location', 'Start Date/Time', 'date',	'start', 'End Date/Time' ,'end','Abstracts bibcode'])
csv_present_auth_writer.writerow(['Author ID', 'Name', 'Sub-Title', 'Description', 'Room/Location'])
csv_linking_writer.writerow(['session_id', 'presentation_id', 'author_id'])

for Session in root.find('SESSIONS'):
    session_id = Session.get('sess_id')
    session_title = Session.find('SESSION_TITLE').text
    session_type = Session.find('SESSION_TYPE').text
    session_notes = Session.find('SESSION_NOTES').text
    
    session_d = Session.find('SESSION_DATE')
    session_year = session_d.find('YEAR').text
    session_date = session_d.find('DAY').text+'/'+session_d.find('MONTH').text+'/'+session_d.find('YEAR').text
    
    session_start_t = Session.find('SESSION_START_TIME')
    session_start_time = session_start_t.find('HOUR').text+':'+session_start_t.find('MINUTE').text+' '+session_start_t.find('AM_PM').text
    
    session_start_date_time = session_date+' '+session_start_time

    session_end_t = Session.find('SESSION_END_TIME')
    session_end_time = session_end_t.find('HOUR').text+':'+session_end_t.find('MINUTE').text+' '+session_end_t.find('AM_PM').text
    
    session_end_date_time = session_date+' '+session_end_time

    session_location = Session.find('SESSION_LOCATION').find('VENUE').text+' '+Session.find('SESSION_LOCATION').find('ROOM').text
    
    csv_session_writer.writerow([session_id, session_title,  session_start_date_time, session_date, session_start_time, session_end_date_time, session_end_time, session_location, session_type, '', '', session_notes])
    #print "data is", repr(Session.findall('PRESENTATIONS'))
    #print session_date, session_start_time, session_end_time, session_location, session_type
    if Session.find('PRESENTATIONS') is not None:
        for present in Session.find('PRESENTATIONS'):

            present_id = present.get('id')

            if present.find('FINAL_ID').text is not None:
                fl_id = present.find('FINAL_ID').text
                final_id = fl_id+' - '
                final_id_bib = fl_id.replace(".","")
            else:
                final_id = ''
                final_id_bib = ''
            
            if present.find('AUTHORS') is not None:
                single_author = present.find('AUTHORS')[0]

                if single_author.find('MNAME').text is not None:
                    m_name = ' '+single_author.find('MNAME').text+' '
                else:
                    m_name = ' '

                author_lst_name = single_author.find('LNAME').text
                present_author = single_author.find('FNAME').text+m_name+author_lst_name
                author_name = author_lst_name+', '+single_author.find('FNAME').text+m_name
                author_id = single_author.get('person_id')
                author_inst = single_author.find('AFFILIATIONS')[0].find('INST').text
                author_lst_name_bib = author_lst_name[0]
                
            else:
                present_author = ''
                author_name = ''
                author_lst_name = ''
            
            present_title = final_id+''+present.find('TITLE').text +'('+present_author+')'
            present_start_t = present.find('PRESENTATION_START_TIME')
            present_start_time = present_start_t.find('HOUR').text+':'+present_start_t.find('MINUTE').text+' '+present_start_t.find('AM_PM').text
    
            present_start_date_time = session_date+' '+present_start_time

            present_end_t = present.find('PRESENTATION_END_TIME')
            present_end_time = present_end_t.find('HOUR').text+':'+present_end_t.find('MINUTE').text+' '+present_end_t.find('AM_PM').text
    
            present_end_date_time = session_date+' '+present_end_time

            print session_id, author_id ,author_name, author_inst

            bib_code = session_year+"AAS...232"+final_id_bib+author_lst_name_bib
            print bib_code
           
            csv_present_writer.writerow([session_id, present_id, present_title, '', '', session_location, present_start_date_time, session_date, present_start_time, present_end_date_time, present_end_time, bib_code])
            csv_present_auth_writer.writerow([author_id, author_name, author_inst, present_title, ''])
            csv_linking_writer.writerow([session_id, present_id, author_id])