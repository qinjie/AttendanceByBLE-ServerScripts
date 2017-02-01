# Validate data which get from excel form and add new data to database

import  Scr05_importVenue
from Scr05_importVenue import  *

# Convert information of Student to array list
def getStudent():
    studentTable = getStudentTable()
    for a in studentTable :
        card = a['card']
        name = a['name']
        acad = a['acad']
        gender = a['gender']
        user_id = a['userID']
        listStudent.append({'card':card, 'name':name, 'gender' : gender, 'acad': acad, 'user':user_id})

# update status of Student(leave or not) and add check student in listStudent is new or have appeared at database
def updateStudent() :
    listCard = []
    for a in listStudent:
        if (a['card'] not in listCard):
            listCard.append(a['card'])

    query = Student.update(disable = 1).where(Student.id > 0)
    query.execute()

    query = Student.update(disable=0).where(Student.card.in_(listCard))
    query.execute()

# Add new user into user table
def addUser() :

    if (len(listUser) > 0):
        try:
            with db.atomic():
                user.insert_many(listUser).execute()
        except IntegrityError:
            print('Aaaa')

# Create new user for new Student (user name = card, password = card, email = S + card Number + @connect.np.edu.sg)
def updateStudentUser() :
    for a in listStudent :
        card = a['card']
        t = 'S'
        for i in range(0, len(card) - 1) :
            t = t + str(card[i])
        email = t + '@connect.np.edu.sg'

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
        card = a.username
        for b in listStudent :
            if (b['card'] == card) :
                b['user'] = a.id

# Validate data of Student list, and delete duplicate Student (base "card" fields)
def validateStudent() :
    _listStudent = sorted(listStudent, key=itemgetter('card'))
    listCard = []

    listStudent.clear()

    for a in _listStudent:
        if (a['card'] not in listCard) :
            listStudent.append(a)
            listCard.append(a['card'])
    # print(len(listStudent))

# add new Student into Student table
def addStudent() :
    count = 0
    _listStudent = sorted(listStudent, key=itemgetter('card'))
    listCurrentStudent = Student
    listCard = []
    for a in listCurrentStudent :
        listCard.append(a.card)
    listStudent.clear()
    # print(len(_listStudent))
    for a in _listStudent :
        if a['card'] not in listCard :
            listStudent.append(a)
    validateStudent()
    updateStudentUser()
    if (len(listStudent) > 0) :
        try :
            with db.atomic():
                Student.insert_many(listStudent).execute()
        except IntegrityError :
            print("Error when insert student")

if __name__ == "__main__" :
    os.system("python Scr05_importVenue.py")
    getStudent()
    updateStudent()
    addStudent()
    print ("Import Student table successfully!")
