# import data to Lecturer table

import Scr06_importStudent
from  Scr06_importStudent import  *

# Convert information of Lecturer to array list
def getLecturer() :
    lecturerTable = getLecturerTable()
    for a in lecturerTable :
        card = a['card']
        name = a['name']
        acad = a['acad']
        email = a['email']
        user_id = a['userID']
        # print(card, name, acad, email, user_id)
        listLecturer.append({'card': card, 'name': name, 'acad': acad, 'email' : email,'user': user_id})
# Validate data of Lecturer list, and delete duplicate Lecturer (base "card" fields)
def validateLecturer() :
    _listLecturer = sorted(listLecturer, key=itemgetter('card'))
    listCard = []
    # print(len(_listStudent))
    listLecturer.clear()
    # print(len(_listStudent))
    for a in _listLecturer:
        if (a['card'] not in listCard) :
            listLecturer.append(a)
            listCard.append(a['card'])

# update status of Lecturer(leave or not) and add check Lecturer in listLecturer is new or have appeared at database
def updateLecturer() :
    listCard = []
    for a in listLecturer:
        if (a['card'] not in listCard):
            listCard.append(a['card'])

    query = Lecturer.update(disable = 1).where(Lecturer.id > 0)
    query.execute()
    query = Lecturer.update(disable = 0).where(Lecturer.card.in_(listCard))
    query.execute()

# create new user for new Lecturer
def updateLecturerUser() :
    listUser.clear()
    for a in listLecturer :
        email = a['email']
        t = a['card']
        hash_object = hashlib.md5(t.encode('utf-8'))
        password = hash_object.hexdigest()
        hash_object = hashlib.md5(email.encode('utf-8'))
        auth_key = hash_object.hexdigest()
        listUser.append(
            {
                'username' : a['card'],
                'auth_key' : auth_key,
                'password_hash' : password,
                'email' : email,
                'name' : a['name'],
            }
        )

    addUser()

    _listUser = user.select()
    for a in _listUser :
        email = a.email
        for b in listLecturer :
            if (b['email'] == email) :
                b['user'] = a.id

# add new lecturer to Lecturer table
def addLecturer() :
    count = 0

    _listLecturer = sorted(listLecturer, key=itemgetter('card'))
    listCurrentLecturer = Lecturer
    listCard = []
    for a in listCurrentLecturer:
        listCard.append(a.card)

    listLecturer.clear()
    for a in _listLecturer:
        if a['card'] not in listCard:
            listLecturer.append(a)

    validateLecturer()
    _listLecturer.clear()
    # print(listLecturer)
    updateLecturerUser()
    if (len(listLecturer) > 0) :
        try :
            with db.atomic():
                Lecturer.insert_many(listLecturer).execute()
        except IntegrityError :
            count += 1
            print('Error when insert Lecturer')

if __name__ == "__main__" :

    os.system("python Scr06_importStudent.py")
    getLecturer()
    updateLecturer()
    addLecturer()
    print("Import lecturer table sucessfully!")