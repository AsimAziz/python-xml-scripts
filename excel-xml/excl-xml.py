
import pandas as pd
import csv
import xlrd 
from pandas import ExcelWriter
from pandas import ExcelFile
import xml.etree.ElementTree as ET
import sys
import xml.dom.minidom
reload(sys)
sys.setdefaultencoding('utf8')
 
source = ("AAS_ADS_DataMapTemplate.xlsx") 
file_obj = open('Session-16-01-2018.xml', 'w')

wb = xlrd.open_workbook(source) 
sheet = wb.sheet_by_index(2) 
sheet.cell_value(0, 0) 
  
rootW = ET.Element("AbstractBook", meetingID="233rd Meeting of the American Astronomical Society")

for i in range(sheet.nrows): 
    session_id_arr = str(sheet.cell_value(i, 0)).split('.')
    session_id = session_id_arr[0]
    SessionNumber_arr = str(sheet.cell_value(i, 1)).split('.')
    SessionNumber = SessionNumber_arr[0]
    SessionTitle = sheet.cell_value(i, 2)
    SessionType = sheet.cell_value(i, 3)
    sessionFullDay = str(sheet.cell_value(i, 4)).split(',')
    sessionDay = sessionFullDay[0]
    SessionTime = sheet.cell_value(i, 7)
    SessionLocation = sheet.cell_value(i, 8)

    pre_uniqueID_arr = str(sheet.cell_value(i, 9)).split('.')
    pre_uniqueID = pre_uniqueID_arr[0]
    PresentationNumber = sheet.cell_value(i, 10)
    pre_title = sheet.cell_value(i, 11)
    AuthorBlockAuthors = str(sheet.cell_value(i, 23))
    AuthorBlockInsts = str(sheet.cell_value(i, 14))
    AuthorBlock = '<div>'+AuthorBlockAuthors+'</div><div>'+AuthorBlockInsts+'<div>'
    print AuthorBlock
    AbstractBody = sheet.cell_value(i, 16)
    #bib_code = sheet.cell_value(i, 12)
    

    if (i == 0 or sheet.cell_value(i, 0) != sheet.cell_value(i-1, 0)):
        sessionDetails = ET.SubElement(rootW, "SessionDetail", uniqueID=str(session_id))
        ET.SubElement(sessionDetails, "SessionNumber").text = str(SessionNumber)
        ET.SubElement(sessionDetails, "SessionTitle").text = str(SessionTitle)
        ET.SubElement(sessionDetails, "SessionTypeName").text = str(SessionType)
        ET.SubElement(sessionDetails, "SessionDay").text = sessionDay
        ET.SubElement(sessionDetails, "SessionTime").text = str(SessionTime)
        ET.SubElement(sessionDetails, "SessionLocation").text = str(SessionLocation)
        presentations = ET.SubElement(sessionDetails, "Presentations")

    presentation = ET.SubElement(presentations, "Presentation", uniqueID=str(pre_uniqueID))
    ET.SubElement(presentation, "PresentationNumber").text = str(PresentationNumber)
    ET.SubElement(presentation, "PresentationTitle").text = str(pre_title)
    ET.SubElement(presentation, "AuthorBlock").text = str(AuthorBlock)
    #ET.SubElement(presentation, "AbstractBibCode").text = str(bib_code)
    ET.SubElement(presentation, "AbstractBody").text = str(AbstractBody)

xml_data =  ET.tostring(rootW, encoding='UTF-8', method='xml')

#write encoded xml data in xml file 
file_obj.write(xml_data)

#close xml file
file_obj.close