# Generate [StudentLeaveLesson] base on [Student_leave] table and [Lesson] table add into db

import Scr15_importAttendance
from Scr15_importAttendance import  *


# Generate Attendance base on lesson_date, lesson, student table
def getStudentLeaveLesson() :
    listStudentLeave = Student_leave.select()
    t = Timetable.select()
    listLsDate = Lesson_date.select()
    listLs = []
    for a in listStudentLeave :
        studentID = a.student_id
        listLs.clear()
        start_date = a.start_date
        end_date = a.end_date
        for b in t :
            if (b.student_id == studentID) :
                listLs.append(b.lesson_id)
        for a in listLs :
            lesson_id  = a
            for b in listLsDate :
                date = b.ldate
                if ((start_date <= date) and (date <= end_date)) :
                    if (b.lesson_id == lesson_id) :
                        listStudentLeaveLesson.append(
                            {
                                'student' : studentID,
                                'lesson_date' : b.id
                            }
                        )

# Import StudentLeaveLesson list to database and reject data if it exist
def addStudentLeaveLesson() :
    _lsll = Student_leave_lesson.select()
    _lls = []
    for a in _lsll :
        t = str(a.student_id) + " " + str(a.lesson_date_id)
        if (t not in _lls) :
            _lls.append(t)
    _listStudentLeaveLesson = []
    for a in listStudentLeaveLesson :
        t = str(a['student']) + " " + str(a['lesson_date'])
        if (t not in _lls) :
            _lls.append((a))
            _listStudentLeaveLesson.append(a)

    listStudentLeaveLesson.clear()
    for a in _listStudentLeaveLesson :
        listStudentLeaveLesson.append(a)

    if (len(listStudentLeaveLesson) > 0) :
        try :
            with db.atomic():
                Student_leave_lesson.insert_many(listStudentLeaveLesson).execute()
        except IntegrityError :
            print('error when insert Student_leave_lesson')

if __name__ == '__main__' :
    os.system("python Scr15_importAttendance.py")
    getStudentLeaveLesson()
    addStudentLeaveLesson()
    print("Generate student_leave_lesson successfully!")