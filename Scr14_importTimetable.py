#  generate Timetable of student base on Lesson table and Student table add into db

import scr13_importLessonLecturer
from scr13_importLessonLecturer import  *


# generate Timetable of student base on Lesson table and Student table
def getTimetable() :
    lesson_list = Lesson.select()
    student_list = Student.select()
    free = []
    d = []
    studentEnd = []
    calendar = ['MON', 'TUES', 'WED', 'THUR', 'FRI', 'SAT', 'SUN']
    for wd in range(2, 9) :
        start = datetime.time(0, 30, 0)
        end = datetime.time(22, 59, 0)
        for i in range(0, len(lesson_list)):
            d.append(0)

        for i in range(0, len(student_list)):
            free.append(0)
            studentEnd.append(datetime.time(0, 0, 0))

        while (start < end):

            for i in range(0, len(student_list)):
                if (studentEnd[i] <= start):
                    free[i] = 1

            for j in range(0, len(lesson_list)):
                lesson = lesson_list[j]
                lesson_id = lesson.id
                startLesson = lesson.start_time
                finishLesson = lesson.end_time
                weekday = lesson.weekday
                # print(weekday, wd)
                if (weekday == calendar[wd - 2]) :
                    if ((startLesson <= start) and (start <= finishLesson)):
                        if (d[j] == 1):
                            continue
                        for i in range(0, len(student_list)):
                            if (free[i] == 1):
                                free[i] = 0
                                studentEnd[i] = finishLesson
                                d[j] = 1
                                listTimetable.append(
                                    {
                                        'lesson': lesson_id,
                                        'student': student_list[i].id
                                    }
                                )
                                break
            start = datetime.time(start.hour + 1, start.minute, start.second)

# add new Timetable to timetable_table and reject data if it exist
def addTimetable() :
    count = 0
    _l = []
    _listTimeTable = []
    _t = Timetable.select()
    for a in _t :
        _l.append(a.lesson_id * 10000 + a.student_id)

    for a in listTimetable :
        t = a['lesson'] * 10000 + a['student']
        if (t not in _l) :
            _listTimeTable.append(a)

    if (len(_listTimeTable) > 0) :
        try:
            with db.atomic():
                Timetable.insert_many(_listTimeTable).execute()
        except IntegrityError:
            count += 1
            print('Error when insert timetable')

if __name__ == '__main__' :
    os.system("python scr13_importLessonLecturer.py")
    getTimetable()
    addTimetable()
    print("Generate Timetable successfully!")