# Generate uuid for each beacon lesson and add into db

import Scr11_generateBeaconUser
from Scr11_generateBeaconUser import  *

# Generate uuid for each beacon lesson
def getBeaconLesson():
    BcL = Beacon_leson.select()
    _num = 10000000;
    _l = []
    for a in BcL :
        if (a.lesson_id not in _l) :
            _l.append(a.lesson_id)

    listLs = Lesson.select()
    for a in listLs :
        if (a.id not in _l) :
            _l.append(a)
            _num += 1
            listBeaconLesson.append(
                {
                    'lesson' : a.id,
                    'uuid' : uuid.uuid4()
                }
            )

# Insert Beaconlesson list to database and reject data if it exist
def addBeaconLesson():
    if (len(listBeaconLesson) > 0):
        try:
            with db.atomic():
                Beacon_leson.insert_many(listBeaconLesson).execute()
        except IntegrityError:
            print('Error when insert beacon_lesson')

if __name__ == '__main__' :
    os.system("python Scr11_generateBeaconUser.py")
    getBeaconLesson()
    addBeaconLesson()
    print("Generate beacon_lesson successfully!")