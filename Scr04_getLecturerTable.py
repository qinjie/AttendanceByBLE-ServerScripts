# Get information of Lecturers from Lecturer sheet

import Scr03_getStudentTable
from Scr03_getStudentTable import  *

def getLecturerTable():
    data = getXlsxData()
    a = data.get_sheet_names()
    lecturers = data.get_sheet_by_name(a[1])
    row_count = lecturers.max_row + 1
    tmp = 1
    for row in range(3, row_count):
        userID = tmp + row
        card = lecturers['B' + str(row)].value
        name = lecturers['C' + str(row)].value
        acad = lecturers['A' + str(row)].value
        email = lecturers['D' + str(row)].value
        moduleID = lecturers['E' + str(row)].value
        offerNbr = lecturers['F' + str(row)].value
        subjectArea = lecturers['G' + str(row)].value
        catalogNbr = lecturers['H' + str(row)].value
        classSection = lecturers['I' + str(row)].value
        component = lecturers['J' + str(row)].value
        facilityID = lecturers['K' + str(row)].value
        day = lecturers['L' + str(row)].value
        lecturerTable.append({
            'userID' : userID,
            'card' : card,
            'name' : name,
            'acad' : acad,
            'email' : email,
            'moduleID' : moduleID,
            'offerNbr' : offerNbr,
            'subjectArea' : subjectArea,
            'catalogNbr' : catalogNbr,
            'classSection' : classSection,
            'component' : component,
            'facilityID' : facilityID,
            'day' : day
        })
    return lecturerTable

if __name__ == "__main__" :
    os.system("python Scr03_getStudentTable.py")
    getLecturerTable()
    print ("Get data from Lecturer sheet successfully!")
