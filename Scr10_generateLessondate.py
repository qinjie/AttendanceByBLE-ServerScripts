# get lesson_dates after semester_date and lesson tables are set up

import Scr09_importLesson
from Scr09_importLesson import  *

# Generate [lesson dates] after [semester date] and [lesson] tables are set up
def getLessondate() :
    list_lesson = Lesson.select()
    list_semester_date = Semester_date.select()
    list_lesson_date = Lesson_date.select()
    calendar = ['MON', 'TUES', 'WED', 'THUR', 'FRI', 'SAT', 'SUN']

    list_ldate = []
    for a in list_lesson_date:
        list_ldate.append(a.ldate)
    list_ldate = list(set(list_ldate))

    for a in list_semester_date:
        weekday = a.weekday
        # print(a.weekday)
        ldate = a.tdate
        if (a.is_holiday == 0) :
            if (ldate not in list_ldate):
                for b in list_lesson:
                    weekday_ = calendar[weekday - 1]
                    if (weekday_ == b.weekday) and (weekday < 6):
                        lesson_id = b.id
                        ldate = a.tdate
                        updated_by = 2;
                        listLessondate.append(
                            {
                                'lesson' : lesson_id,
                                'ldate' : ldate,
                                'updated_by' : updated_by
                            }
                        )

# Insert list of Lessondate  to database and reject data if it exist
def addLessondate() :
    count = 0
    # print(listLessondate)
    if (len(listLessondate) > 0) :
        try:
            with db.atomic():
                Lesson_date.insert_many(listLessondate).execute()
        except IntegrityError:
            count += 1
            print('Error when insert lesson_date')

if __name__ == '__main__' :
    os.system("python Scr09_importLesson.py")
    getLessondate()
    addLessondate()
    print("Generate lesson date successfully!")