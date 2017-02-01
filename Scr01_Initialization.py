# Connect to database and create new table if table doesn't exist
# Import library
# Declare class Model class

from operator import itemgetter

import openpyxl
import os
import datetime
import uuid
import hashlib

from peewee import *

db = MySQLDatabase('test')
# Link to folder contain excel form
directoryPath = r'C:\Users\Champ\Desktop\Python\Proj'
listLecturer = []
listStudent = []
studentTable = []
lecturerTable = []
listLesson = []
listLessonLecturer = []
listTimetable = []
listAttendance = []
listSemesterdate = []
listLessondate = []
listBeaconLesson = []
listBeaconUser = []
listVenue = []
listUser = []
listStudentLeaveLesson = []


class user(Model):
    username = CharField(unique=True)
    auth_key = CharField(max_length=32)
    device_hash = CharField(unique=True, null=True)
    password_hash = CharField()
    email = CharField(unique=True)
    profileImg = CharField(null=True)
    status = SmallIntegerField(default=10)
    role = SmallIntegerField(default=10)
    name = CharField(null=True)
    face_id = CharField(max_length=1000, null=True)
    person_id = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now(), null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db


class Student(Model):
    card = CharField(max_length=15, unique=True)
    name = CharField(max_length=255)
    gender = CharField(max_length=1)
    acad = CharField(max_length=10)
    user = ForeignKeyField(user, unique=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(null=True)
    disable = IntegerField(default=0)

    class Meta:
        database = db


class Lecturer(Model):
    card = CharField(max_length=15, unique=True)
    name = CharField(max_length=255)
    acad = CharField(max_length=10)
    email = CharField(max_length=255)
    user = ForeignKeyField(user)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(null=True)
    disable = IntegerField(default=0)

    class Meta:
        database = db


class venue(Model):
    location = CharField(max_length=100)
    name = CharField(max_length=100, null=True)
    uuid = CharField(max_length=40, null=True)
    major = SmallIntegerField(null=True)
    minor = SmallIntegerField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(null=True)

    class Meta:
        indexes = (
            (('uuid', 'major', 'minor'), True),
        )
        database = db


class Lesson(Model):
    semester = CharField(max_length=10)
    module_id = CharField(max_length=10)
    subject_area = CharField(max_length=10)
    catalog_number = CharField(max_length=10)
    class_section = CharField(max_length=5)
    component = CharField(max_length=5)
    facility = CharField(max_length=15)
    venue = ForeignKeyField(venue, index=True)
    weekday = CharField(max_length=5)
    start_time = TimeField()
    end_time = TimeField()
    meeting_pattern = CharField(max_length=5, null=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('semester', 'module_id', 'class_section', 'weekday', 'start_time'), True),
        )
        database = db


class Lesson_lecturer(Model):
    lesson = ForeignKeyField(Lesson, index=True)
    lecturer = ForeignKeyField(Lecturer, related_name='Lecturer.id', index=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('lesson', 'lecturer'), True),
        )
        database = db


class Timetable(Model):
    lesson = ForeignKeyField(Lesson, index=True)
    student = ForeignKeyField(Student, related_name='Student.id', index=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('lesson', 'student'), True),
        )
        database = db


class Lesson_date(Model):
    lesson = ForeignKeyField(Lesson, index=True)
    ldate = DateField()
    updated_by = IntegerField(default=0, index=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('lesson', 'ldate'), True),
        )
        database = db


class Attendance(Model):
    student = ForeignKeyField(Student, index=True)
    lesson_date = ForeignKeyField(Lesson_date, index=True)
    recorded_time = TimeField(default=datetime.datetime.now().time())
    lecturer = ForeignKeyField(Lecturer, index=True)
    status = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('student', 'lesson_date'), True),
        )
        database = db


class Semester_info(Model):
    name = CharField(max_length=20)
    start_date = DateField()
    end_date = DateField()
    break_start = DateField()
    break_end = DateField()
    status = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


class Semester_date(Model):
    semester = ForeignKeyField(Semester_info, index=True)
    tdate = DateField(unique=True)
    week_num = IntegerField()
    weekday = IntegerField()
    is_holiday = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


class Beacon_leson(Model):
    lesson = ForeignKeyField(Lesson, unique=True)
    uuid = CharField(default=uuid.uuid4(), unique=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


class Public_holiday(Model):
    year = IntegerField()
    name = CharField(max_length=30)
    hdate = DateField()
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta():
        database = db


class Beacon_attendance_lecturer(Model):
    lesson_date = ForeignKeyField(Lesson_date, index=True)
    student = ForeignKeyField(Student, index=True)
    lecturer = ForeignKeyField(Lecturer, index=True)
    status = BooleanField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('lesson_date', 'student'), True),
        )
        database = db


class Beacon_attendance_student(Model):
    lesson_date = ForeignKeyField(Lesson_date, index=True)
    student_id_1 = ForeignKeyField(Student, index=True)
    status = BooleanField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('lesson_date', 'student_id_1'), True),
        )
        database = db


class Beacon_user(Model):
    user = ForeignKeyField(user, unique=True)
    major = SmallIntegerField()
    minor = SmallIntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('major', 'minor'), True),
        )
        database = db


class Student_leave(Model):
    student = ForeignKeyField(Student, null=False, index=True)
    start_date = DateField(null=False)
    end_date = DateField(null=False)
    remark = CharField(max_length=100, null=False)
    status = SmallIntegerField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(null=True)

    class Meta:
        indexes = (
            (('student', 'start_date'), True),
        )
        database = db


class Student_leave_lesson(Model):
    student = ForeignKeyField(Student, index=True)
    lesson_date = ForeignKeyField(Lesson_date, index=True)
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('student', 'lesson_date'), True),
        )
        database = db


class User_token(Model):
    user = ForeignKeyField(user, index=True)
    token = CharField(unique=True)
    title = CharField()
    ip_address = CharField()
    expire_date = DateTimeField()
    action = SmallIntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


def initialization() :
    db.connect()
    db.create_tables([user], safe=True)
    db.create_tables([Semester_info], safe=True)
    db.create_tables([Public_holiday], safe=True)
    db.create_tables([Semester_date], safe=True)
    db.create_tables([venue], safe=True)
    db.create_tables([Lesson], safe=True)
    db.create_tables([Lesson_date], safe=True)
    db.create_tables([Student], safe=True)
    db.create_tables([Lecturer], safe=True)
    db.create_tables([Lesson_lecturer], safe=True)
    db.create_tables([Timetable], safe=True)
    db.create_tables([Attendance], safe=True)
    db.create_tables([Beacon_leson], safe=True)
    db.create_tables([User_token], safe=True)
    db.create_tables([Beacon_user], safe=True)
    db.create_tables([Beacon_attendance_lecturer], safe=True)
    db.create_tables([Beacon_attendance_student], safe=True)
    db.create_tables([Student_leave], safe=True)
    db.create_tables([Student_leave_lesson], safe=True)


if __name__ == "__main__" :
    initialization()
    print("Initialize table successfully")