# Generate Attendance base on lesson_date, lesson, student table add into db

import Scr14_importTimetable
from Scr14_importTimetable import  *


# Generate Attendance base on lesson_date, lesson, student table
def getAttendance() :
    lsdate = Lesson_date.select()
    timetb = Timetable.select()
    lslec = Lesson_lecturer.select()
    for a in lsdate :
        lsID = a.lesson_id
        lcID = 0
        for b in lslec :
            if (b.lesson_id == lsID):
                lcID = b.lecturer_id

        for b in timetb :
            if (lsID == b.lesson_id):
                listAttendance.append(
                    {
                        'student' : b.student_id,
                        'lesson_date' : a.id,
                        'recorded_time' : datetime.datetime.now().time(),
                        'lecturer' : lcID,
                        'status' : lsID
                    }
                )

# Insert attendance list to database and reject data if it exist
def addAttendance() :
    count = 0
    _listAttendance = []
    _l = []
    _t = Attendance.select()
    for a in _t :
        t = str(a.student_id) + " " + str(a.lesson_date_id)
        _l.append(t)

    for a in listAttendance :
        t = str(a['student']) + " " + str(a['lesson_date'])
        if (t not in _l) :
            _listAttendance.append(a)

    if (len(_listAttendance) > 0) :
        try:
            with db.atomic():
                Attendance.insert_many(_listAttendance).execute()
        except IntegrityError:
            count += 1
            print('Error when insert attendance')

if __name__ == '__main__' :
    os.system("python Scr14_importTimetable.py")
    getAttendance()
    addAttendance()
    print("Generate attendance successfully!")