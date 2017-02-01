# Get information of students from Student sheet

import  Scr02_GetXlsxData
from Scr02_GetXlsxData import  *

def getStudentTable() :
    data = getXlsxData()
    a = data.get_sheet_names()
    students = data.get_sheet_by_name(a[0])
    row_count = students.max_row + 1
    tmp = 1;
    for row in range(3, row_count):
        card = students['B' + str(row)].value
        name = students['C' + str(row)].value
        acad = students['A' + str(row)].value
        gender = 'M'
        moduleID = students['D' + str(row)].value
        offerNbr = students['E' + str(row)].value
        subjectArea = students['F' + str(row)].value
        catalogNbr = students['G' + str(row)].value
        classSection = students['H' + str(row)].value
        component =  students['I' + str(row)].value
        facilityID = students['J' + str(row)].value
        day = students['K' + str(row)].value
        startTime = students['L' + str(row)].value
        endTime = students['M' + str(row)].value
        meetingPattern = students['N' + str(row)].value
        userID = row + tmp
        studentTable.append({
            'card' : card,
            'name' : name,
            'acad' : acad,
            'gender' : gender,
            'moduleID' : moduleID,
            'offerNbr' : offerNbr,
            'subjectArea' : subjectArea,
            'catalogNbr' : catalogNbr,
            'classSection' : classSection,
            'component' : component,
            'facilityID' : facilityID,
            'Day' : day,
            'startTime' : startTime,
            'endTime' : endTime,
            'meetingPattern' : meetingPattern,
            'userID' : userID
        })
    return studentTable

if __name__ == '__main__' :
    os.system("python Scr02_GetXlsxData.py")
    getStudentTable()
    print ("Get data from Student sheet successfully!")