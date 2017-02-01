# get lesson base on Student sheet and add into db
import Scr08_generateSemesterdate
from Scr08_generateSemesterdate import  *

# get lesson base on Student sheet
def getLesson() :
    studentTable = getStudentTable()
    for a in studentTable :
        semester = 2
        moduleID = a['moduleID']
        subjectArea = a['subjectArea']
        catalogNumber = a['catalogNbr']
        classSection = a['classSection']
        component = a['component']
        facility = a['facilityID']
        venueID = 1
        weekDay = a['Day']
        startTime = a['startTime']
        endTime = a['endTime']
        meetingPattern = a['meetingPattern']
        listLesson.append({'semester': semester,
                           'module_id': moduleID,
                           'subject_area': subjectArea,
                           'catalog_number': catalogNumber,
                           'class_section': classSection,
                           'component' : component,
                           'facility' : facility,
                           'venue' : venueID,
                           'weekday' : weekDay,
                           'start_time' : startTime,
                           'end_time' : endTime,
                           'meeting_pattern' : meetingPattern
                           })

# Validate and add new lesson into lesson table and reject data if it exist
def addLesson() :
    _listLesson = []
    for a in listLesson :
        if (a not in _listLesson) :
            _listLesson.append(a)
    listLesson.clear()
    for a in _listLesson :
        listLesson.append(a)

    _listLesson.clear()
    _ltt = []
    _listLesson = Lesson.select()

    for a in _listLesson :
        t = str(str(a.semester) + " " + a.module_id +" " +  a.class_section + " "  + a.weekday + " " + str(a.start_time))
        # print(t)
        _ltt.append(t)

    # print(_ltt)
    _listLessont = []
    for a in listLesson :
         t = str(str(a['semester']) + " " + a['module_id'] + " "  + a['class_section'] + " " +  a['weekday'] + " " + str(a['start_time']) + ":00")
         # print(t)
         if (t not in _ltt) :
            _ltt.append(t)
            _listLessont.append(a)

    count = 0

    # print(_listLessont)
    if (len(_listLessont)> 0 ):
        try:
            with db.atomic():
                Lesson.insert_many(_listLessont).execute()
        except IntegrityError:
            print("Error when insert lesson")

if __name__ == '__main__' :
    os.system("python Scr08_generateSemesterdate.py")
    getLesson()
    addLesson()
    print("Generate lesson successfully!")