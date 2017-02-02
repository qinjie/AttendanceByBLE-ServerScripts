#Generate data of venue and add venue's data to database

import Scr04_getLecturerTable
from Scr04_getLecturerTable import  *

# Generate venue data(location, name)
def getVenue() :
    studentTable = getStudentTable()
    _l = []
    for a in studentTable :
        _l.append(a['facilityID'])

    _listVenue = list(set(_l))
    for a in _listVenue :
        listVenue.append(
            {
                'location' : a,
                'name' : a
            }
        )

# Add venue list to database and reject data if it exist
def addVenue() :
    lVn = venue.select()
    l = []
    for a in lVn :
        t = a.uuid + " " + str(a.major) + " " + str(a.minor)
        if (t not in l) :
            l.append(t)

    # _listVenue = []
    # for a in listVenue:
    #     t = a['uuid'] + " " + str(a['major']) + " " + str(a['minor'])
    #     if (t not in l ) :
    #         _listVenue.append(a)
    #
    # listVenue.clear()
    # for a in _listVenue :
    #     listVenue.append(a)
    # print(listVenue)
    if (len(listVenue) > 0):
        try:
            with db.atomic():
                venue.insert_many(listVenue).execute()
        except IntegrityError:
            print('Error when insert venue')


if __name__ == "__main__" :
    os.system("python Scr04_getLecturerTable.py")
    getVenue()
    addVenue()
    print ("Import venue data succesfully!")