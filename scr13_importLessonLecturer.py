#  Generate lesson lecturer base on Lesson table and Lecturer table add into db

import Scr12_generateBeaconLesson
from Scr12_generateBeaconLesson import  *

# Generate lesson lecturer base on Lesson table and Lecturer table
def getLessonLecturer() :
    lesson_list = Lesson.select()
    lecturer_list = Lecturer.select()

    start = datetime.time(0, 30, 0)
    end = datetime.time(22, 59, 0)
    free = []
    d = []
    for i in range (0, len(lesson_list)) :
        d.append(0)

    lecturerEnd = []

    for i in range(0, len(lecturer_list)) :
        free.append(0)
        lecturerEnd.append(datetime.time(0, 0, 0))

    while (start < end) :

        for i in range(0, len(lecturer_list) ):
            if (lecturerEnd[i] <= start) :
                free[i] = 1

        for j in range(0, len(lesson_list)) :
            lesson = lesson_list[j]
            lesson_id = lesson.id
            startLesson = lesson.start_time
            finishLesson = lesson.end_time
            if ((startLesson <= start) and (start <= finishLesson)) :
                if (d[j] == 1) :
                    continue
                for i in range(0, len(lecturer_list)):
                    if (free[i] == 1):
                        free[i] = 0
                        lecturerEnd[i] = finishLesson
                        d[j] = 1
                        listLessonLecturer.append(
                            {
                                'lesson': lesson_id,
                                'lecturer': lecturer_list[i].id
                            }
                        )
                        break
        start = datetime.time(start.hour + 1, start.minute, start.second)

# Add new Lesson Lecturer to lesson_lecturer_table and reject data if it exist
def addLessonLecturer() :
    _lID = Lesson_lecturer.select()
    _list = []
    _listLsLt = []
    for a in _lID :
        _list.append(a.lesson_id)
    for a in listLessonLecturer :
        if (a['lesson'] not in _list) :
            _list.append(a['lesson'])
            _listLsLt.append(a)

    listLessonLecturer.clear()
    for a in _listLsLt :
        listLessonLecturer.append(a)

    count = 0
    if (len(listLessonLecturer) > 0) :
        try:
            with db.atomic():
                Lesson_lecturer.insert_many(listLessonLecturer).execute()
        except IntegrityError:
            count += 1
            print('Error when insert lesson_lecturer')

if __name__ == '__main__' :
    os.system("python Scr12_generateBeaconLesson.py")
    getLessonLecturer()
    addLessonLecturer()
    print("Generate lesson_lecturer successfully!")