# Generate [semester dates] after [public holiday] and [semster info] tables are setup

import Scr07_importLecturer
from  Scr07_importLecturer import  *


# Generate [semester dates] after [public holiday] and [semster info] tables are setup
def getSemesterdate():
    public_holiday = Public_holiday.select()
    semester_date = Semester_date.select()
    semester_info = Semester_info.select()
    list_holiday = [];
    for a in public_holiday:
        list_holiday.append(a.hdate)

    list_semester_id = []
    for a in semester_date:
        list_semester_id.append(a.semester_id)
    list_semester_id = list(set(list_semester_id))

    for a in semester_info:
        semester_id = a.id
        if (a.status == 0) :
            continue
        if (semester_id not in list_semester_id):
            start_date = a.start_date
            end_date = a.end_date
            week_num = 0;
            while start_date <= end_date:
                tdate = start_date;
                if ((a.break_start <= tdate) and (tdate <= a.break_end)) :
                    start_date += datetime.timedelta(days=1)
                    continue
                weekday = tdate.isoweekday()
                week_num += (weekday == 1)
                start_date += datetime.timedelta(days=1)
                if tdate in list_holiday:
                    is_holiday = 1
                else:
                    is_holiday = 0
                listSemesterdate.append(
                    {
                        'semester' : semester_id,
                        'tdate' : tdate,
                        'week_num' : week_num,
                        'weekday' : weekday,
                        'is_holiday' : is_holiday
                    }
                )

#  Insert list of Semesterdates  to database and reject data if it exist
def addSemesterdate() :
    count = 0
    if (len(listSemesterdate) > 0) :
        try:
            with db.atomic():
                Semester_date.insert_many(listSemesterdate).execute()
        except IntegrityError:
            count += 1
            print('Error when insert semesterdate')

if __name__ == '__main__' :
    os.system("python Scr07_importLecturer.py")
    getSemesterdate()
    addSemesterdate()
    print("Generate Semester date successfully!")