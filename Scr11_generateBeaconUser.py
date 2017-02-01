#Generate uuid, major, minor for Beacon user and add into db

import Scr10_generateLessondate
from Scr10_generateLessondate import  *

# Generate uuid, major, minor for Beacon user
def getBeaconUser() :
    BcU = Beacon_user.select()
    l = []
    for a in BcU :
        if (a.user_id not in l) :
            l.append(a.user_id)

    listUser = user.select()
    _minor = len(l) + 1;
    _major = 99 - len(l) - 1;
    for a in listUser :
        if (a.id not  in l ) :
            l.append(a)
            _minor += 1
            _major -= 1
            listBeaconUser.append(
                {
                    'user' : a.id,
                    'major' : _major,
                    'minor' : _minor
                }
            )

# Insert BeaconUser list to database and reject data if it exist
def addBeaconUser() :
    count = 0
    if (len(listBeaconUser) > 0) :
        try:
            with db.atomic():
                Beacon_user.insert_many(listBeaconUser).execute()
        except IntegrityError:
            count += 1
            print('Error when insert beacon_user')

if __name__ == '__main__' :
    os.system("python Scr10_generateLessondate.py")
    getBeaconUser()
    addBeaconUser()
    print("Generate beacon_user successfully!")