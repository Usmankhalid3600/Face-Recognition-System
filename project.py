import cv2
import os
import sys
import numpy as np
from PIL import Image
from datetime import datetime


def IsRequiredLengthInput(value, length):
    if(len(value) != 4):
        return False


def IsNumber(value):
    for x in value:
        if(ord(x) < 48 or ord(x) > 57):
            return False


def GetValidFallValue():
    value = input('\nEnter fall year of student (YYYY): ')
    while(IsRequiredLengthInput(value, 4) == False or IsNumber(value) == False):
        print("............................please enter correct year information.")
        value = input('\nEnter fall year of student (YYYY): ')
    return value


def GetValidClassValue():
    value = input('\nEnter class (IT/CS/SE): ')
    while (1):
        if(value == 'It' or value == 'It' or value == 'it' or value == 'IT' or value == 'cS' or value == 'Cs' or value == 'cs' or value == 'CS' or value == 'se' or value == 'SE' or value == 'sE' or value == 'Se'):
            return value.upper()
        print("............................please enter correct class information.")
        value = input('\nEnter class (IT/CS/SE) or (it/cs/se): ')


def GetValidRollNumberValue():
    value = input('\nEnter roll number of student: ')

    while (IsNumber(value) == False):
        print("............................please enter correct roll number information.")
        value = input('\nEnter roll number of student: ')
    return value


def IsAlphabet(charValue):
    if((ord(charValue) > 64 and ord(charValue) < 91) or (ord(charValue) > 96 and ord(charValue) < 123)):
        return True
    return False


def IsValidNameString(value):
    for x in value:
        if(IsAlphabet(x) == False):
            return False
    return True


def GetValidStudentName():
    value = input('\nEnter name of student: ')
    while (IsValidNameString(value) == False):
        print("............................please enter correct name information.")
        value = input('\nEnter name of student: ')
    return value


def GetValidNumberOfStudenetValue():
    value = input('\nEnter number of students to add in class: ')
    while(IsNumber(value) == False):
        print("............................please enter correct number of student value,(Hint, Integer).")
        value = input('\nEnter number of students to add in class: ')
    return value


def addStudent():

    Fall = GetValidFallValue()
    Class = GetValidClassValue()
    Id = GetValidRollNumberValue()
    name = GetValidStudentName()
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640) 
    cam.set(4, 480)  
    face_detector = cv2.CascadeClassifier(
        'system/haarcascade_frontalface_default.xml')
    count = 0
    while(True):

        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x+15, y+15), (x+w-20, y+h+10), (255, 0, 0), 3)
            count += 1

            cv2.imwrite("system/classes/" + Fall + "/" + Class + "/" + name +
                        "." + str(Id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])

            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff  

        if count >= 30:  
            break

    cam.release()
    cv2.destroyAllWindows()
    x = input('\nStudent added successfully!\nPress return key to continue!\n')


def addClass():

    Fall = GetValidFallValue()
    Class = GetValidClassValue()
    number = GetValidNumberOfStudenetValue()
    num = 1

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  
    cam.set(4, 480) 
    face_detector = cv2.CascadeClassifier('system/haarcascade_frontalface_default.xml')

    numb = int(number)

    while num <= numb:

        Id = GetValidRollNumberValue()
        name = GetValidStudentName()

        count = 0

        while(True):

            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                

                cv2.rectangle(img, (x+15, y+15), (x+w-20, y+h+10), (255, 0, 0), 3)
                count += 1

                cv2.imwrite("system/classes/" + Fall + "/" + Class + "/" + name +
                            "." + str(Id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])

                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff

            if count >= 30:  
                break

        num += 1

    cam.release()
    cv2.destroyAllWindows()


def get_data(path):

    detect = cv2.CascadeClassifier("system/haarcascade_frontalface_default.xml")
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []
    names = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')  # grayscale
        #print(PIL_img)
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        name = str(os.path.split(imagePath)[-1].split(".")[0])
        faces = detect.detectMultiScale(img_numpy)
        # print(faces)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
        names.append(name)
    # print(faceSamples)
    # print(ids)
    return faceSamples, ids, names


def attendance(fall, section, idnames):

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('system/data.yml')
    cascadePath = "system/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  
    cam.set(4, 480) 
   
    #date = datetime.date(datetime.now())
    #name = section + "/" + fall + "/" + date + ".txt"
    attend = {}
    while True:
        ret, img = cam.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
         
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x+15, y+15), (x+w-20, y+h+10), (255, 0, 0), 3)
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            if (confidence < 50):

                name = idnames.get(id)
                cv2.putText(img, "Id = " + str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)

                cv2.putText(img, "Name = " + name, (x+5, y+h+30), font, 1, (255, 255, 255), 2)

                if id not in attend:
                    attend[id] = name

            else:
                name = "Student not found!"
                cv2.putText(img, name, (x+5, y-5), font, 1, (255, 255, 255), 2)

        cv2.imshow('Attendence in progess', img)
        k = cv2.waitKey(10) & 0xff 
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    write(fall, section, attend, idnames)


def write(fall, section, attend, idnames):

    dat = str(datetime.date(datetime.now()))
    name = "attendence/" + fall + "/" + section + "/" + dat + " .txt"

    f = open(name, "w")
    f.write("Id\t\tName\t\tStatus\n\n")
    for key, value in attend.items():
        f.write(str(key) + "\t\t" + str(value) + "\t\t" + "P\n")
        del idnames[key]

    for key, value in idnames.items():
        f.write(str(key) + "\t\t" + str(value) + "\t\t" + "A\n")

    print("done!")


def markAttendance(fall, section):

    print("Please wait ..........")
    path = "system/classes/" + fall + "/" + section
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Id, names = get_data(path)
    try:
        recognizer.train(faces, np.array(Id))

    except:
        x = input('No Student Data found!\nPress return key to continue .......')
        sys.exit()

    recognizer.write('system/data.yml')
    idnames = {}

    count = 0

    while count < len(names):

        if(count % 30 == 0):
            0
            idnames[Id[count]] = names[count]
            count += 1

        else:
            count += 1

    attendance(fall, section, idnames)


print("Select option\n")
print("1. Add a student in class.\n")
print("2. Add multiple students in a class.\n")
print("3. Mark attendece of a class.\n")

inp = input()

if inp == "1":

    addStudent()

elif inp == "2":

    addClass()

elif inp == "3":

    fall = input('\nEnter fall year of class: ')
    section = input('\nEnter section (IT/CS/SE): ')
    markAttendance(fall, section)


else:

    sys.exit()
