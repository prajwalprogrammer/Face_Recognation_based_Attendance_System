from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView, UpdateView,TemplateView
from core.forms import SignUpForm, ProfileForm,UserProfile
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
import cv2,os
import csv
from tkinter import messagebox as mess
import tkinter as tk
import numpy as np
from PIL import Image
import datetime
import time
import pandas as pd
from .models import UserProfile as up
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django_user import settings
from django_user.settings import EMAIL_HOST_USER
import random
import math
from threading import Timer
from prompt_toolkit import prompt
from tkinter import simpledialog


application_window = tk.Tk()

AuthCode=""
# Sign Up View
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'commons/signup.html'

# Edit Profile View
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'



class ProfileView1(UpdateView):
    model = up
    # form_classes = {'form': ProfileForm,
    #                 'form1': UserProfile,
    #                 }
    form_class = UserProfile
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'

class HomePageView(TemplateView):
    template_name = "index.html"


class AboutPageView(TemplateView):
    template_name = "about.html"

def about(request):
    messages.success(request, 'Your profile was successfully updated!')
    # messages.error(request, "Your profile is updated successfully!")
    return render(request,'auth/aboutus.html')
    


def displayattendance(request):
    return render(request,'auth/attendance.html')
    


def index(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # profile_form = UserProfile(request.POST)
        if form.is_valid() and profile_form.is_valid():
            post = form.save()
            # profilepost = profile_form.save(commit=False)
            # profilepost.user=post 
            post.user = request.user 
            post.save()
            # profilepost.save()
            return redirect('login')
    else:
        form = SignUpForm()
        profile_form=UserProfile()
    context = {'form' : form,'profile_form':profile_form}

    return render_to_response('commons/signup.html',context,  RequestContext(request))
#   return render(request, 'commons/signup.html', context)


def clearToken():
    global AuthCode
    AuthCode=""


@login_required
def home(request):
    return render(request, "auth/login.html", {})
def profile(request):
    if request.method == 'POST':
        digits = [i for i in range(0, 10)]

        ## initializing a string
        
        global AuthCode
        AuthCode=""
        for i in range(6):
            index = math.floor(random.random() * 10)
            AuthCode += str(digits[index])
        r = Timer(300.0, clearToken)
        r.start()
        ## displaying the random string
        print(AuthCode)
        return render(request, 'auth/profile.html', {'data':AuthCode })
    else:
        return render(request, "login/stud_att.html", {})
 
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        form1 = UserProfile(request.POST)
        if form.is_valid() and form1.is_valid():
            user=form.save()
            profile=form1.save(commit=False)
            profile.user=user
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        form1=UserProfile()
    return render(request, 'auth/register.html', {'form': form,'form1':form1})

########################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def check_haarcascadefile():
    print("cbcvb",os.path)
    # directory = r'D:\How-to-use-Built-In-Login-and-Logout-Authentication-System-in-Django'
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        # window.destroy()


def TakeImage(request):
    if request.user.first_name=="":
        messages.error(request, 'please register someone first!')
    else:
        print(request.user.first_name)
        print(request.user.userprofile.year)
        details = "StudentDetails/"+request.user.userprofile.year+"/"
        detailsCSV = "StudentDetails/"+request.user.userprofile.year+"/StudentDetails.csv"
        check_haarcascadefile()
        columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
        assure_path_exists(details)
        assure_path_exists("TrainingImage/")
        directory = r'D:\How-to-use-Built-In-Login-and-Logout-Authentication-System-in-Django\Images'

        serial = 0
        exists = os.path.isfile(detailsCSV)
        if exists:
            with open(detailsCSV, 'r') as csvFile1:
                reader1 = csv.reader(csvFile1)
                for l in reader1:
                    serial = serial + 1
            serial = (serial // 2)
            csvFile1.close()
        else:
            with open(detailsCSV, 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(columns)
                serial = 1
            csvFile1.close()
        Id = str(request.user.userprofile.prn)
        name = request.user.first_name+" "+request.user.last_name
        if ((name.isalpha()) or (' ' in name)):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    # display the frame
                    cv2.imshow('Taking Images', img)
                # wait for 100 miliseconds
                
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Taken for ID : " + Id
            row = [serial, '', Id, '', name]
            with open(detailsCSV, 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            print(res)
            messages.success(request, 'Image taken successfully!')
            TrainImages(request)
        else:
            if (name.isalpha() == False):
                res = "Enter Correct name"
                # message.configure(text=res)
    return redirect('pdata')




def TrainImages(request):
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        messages.error(request, 'please register someone first!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    messages.success(request, 'Your profile Trained successfully !')
    print('Total Registrations till now  : ' + str(ID[0]))
    # return HttpResponseRedirect(reverse_lazy("pdata"))



def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


############### Take Attributes #############
def TrackImages(request):
    if request.user.first_name=="":
        messages.error(request, 'please register your face first!')
    else:
        # text = prompt("Enter Verification Code!!")
        # if text == AuthCode:   
        detailsAtte = "Attendance/"+request.user.userprofile.year+"/"
        detailsCSVAtte = "Attendance/"+request.user.userprofile.year+"/StudentDetails.csv"
        
        details = "StudentDetails/"+request.user.userprofile.year+"/"
        detailsCSV = "StudentDetails/"+request.user.userprofile.year+"/StudentDetails.csv"
        check_haarcascadefile()
        assure_path_exists("Attendance/"+request.user.userprofile.year)
        assure_path_exists("StudentDetails/"+request.user.userprofile.year)
        # for k in tv.get_children():
        #     tv.delete(k)
        msg = ''
        i = 0
        j = 0
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
        exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
        if exists3:
            recognizer.read("TrainingImageLabel\Trainner.yml")
        else:
            messages.error(request, 'Please click on Save Profile to reset data!!')
            return
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
        exists1 = os.path.isfile(detailsCSV)
        if exists1:
            df = pd.read_csv(detailsCSV)
        else:
            messages.error(request, 'Students details are missing, please check!')
            cam.release()
            cv2.destroyAllWindows()
            # window.destroy()
        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if (conf < 50):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                    ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                    ID = str(ID)
                    ID = ID[1:-1]
                    bb = str(aa)
                    bb = bb[2:-2]
                    attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

                else:
                    Id = 'Unknown'
                    bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
            cv2.imshow('Taking Attendance', im)
            if (cv2.waitKey(1) == ord('q')):
                break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        pathAttenda="Attendance\_"+request.user.userprofile.year +"__" + date + ".csv"
        allAttendances="Attendance\_"+request.user.userprofile.year +" Year" + ".csv"
        exists = os.path.isfile(pathAttenda)
        existAtten = os.path.isfile(allAttendances)
        if exists and existAtten:
            with open(pathAttenda, 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',,')
                    nameList.append(entry[0])
                    print(nameList)
                if str(request.user.userprofile.prn) not in nameList:
                    with open(pathAttenda, 'a+') as csvFile1:
                        writer = csv.writer(csvFile1)
                        writer.writerow(attendance)
                    csvFile1.close()
            # with open(pathAttenda, 'a+') as csvFile1:
            #     writer = csv.writer(csvFile1)
            #     writer.writerow(attendance)
            # csvFile1.close()
            with open(allAttendances, 'a+') as csvFile2:
                writer = csv.writer(csvFile2)
                writer.writerow(attendance)
            csvFile2.close()
        else:
            with open(pathAttenda, 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(col_names)
                writer.writerow(attendance)
            csvFile1.close()
            with open(allAttendances, 'a+') as csvFile2:
                writer = csv.writer(csvFile2)
                writer.writerow(col_names)
                writer.writerow(attendance)
            csvFile2.close()
        with open(pathAttenda, 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                i = i + 1
                if (i > 1):
                    if (i % 2 != 0):
                        iidd = str(lines[0]) + '   '
                        # tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
        csvFile1.close()
        cam.release()
        cv2.destroyAllWindows()
        messages.success(request, 'Attendance Marked successfully!')
        # else:
        #     messages.error(request, 'Invalid Code!')

    return HttpResponseRedirect(reverse('pdata'))

def GenerateCode(request):
    digits = [i for i in range(0, 10)]

    ## initializing a string
    
    global AuthCode
    
    for i in range(6):
        index = math.floor(random.random() * 10)
        AuthCode += str(digits[index])

    ## displaying the random string
    print(AuthCode)
    return render(request, 'auth/profile.html', {'form':AuthCode })

######################
allAttendances=''

def desplayAttendance(request):
    global allAttendances
    allAttendances="Attendance\_Second Year" + ".csv"
    if request.method == 'POST':
        print(request.POST['optionsRadios'])
        year=request.POST['optionsRadios']
        date_input = request.POST['date']
        datetimeobject = datetime.datetime.strptime(date_input,'%Y-%m-%d')
        datetimeobject = datetimeobject.strftime('%d-%m-%Y')
        print(datetimeobject)
        allAttendances="Attendance\_"+year+"__"+datetimeobject + ".csv"
        existAtten = os.path.isfile(allAttendances)
        print(existAtten)
        if existAtten:
            with open(allAttendances, 'r') as read_obj:
                read_file = csv.reader(read_obj)

                def fun(variable):
                    # print(variable[0])
                    letters = str(request.user.userprofile.prn)
                    if (variable[0] in letters):
                        # print(letters)

                        return True
                    else:
                        return False
                # filtered = filter(fun, read_file)
                reader = csv.reader(open(allAttendances, 'r'),delimiter=' ')
                filtered = filter(lambda p: request.user.userprofile.prn == p[0], reader)
                print(read_file)
                if request.user.is_staff:
                    context = {'data': read_file}
                else:
                    context = {'data': filtered}
                print("gvgv",context)
                return render(request, 'login/show_attendance.html', context)
    else:
        return render(request, 'login/show_attendance.html')


#############Send Mail##########


def send_email(request):
    print(allAttendances)
    subject = allAttendances
    message = "Hi, \nPlease find the attached csv containing attendance Record."
    email = "shruti.devshatwar21@vit.edu"

    try:
        file2=open(allAttendances,"r")
        mail = EmailMessage(subject, message,settings.EMAIL_HOST_USER, [email])
        mail.attach(allAttendances, file2.read(), 'text/csv')
        print("\nSending email..")
        mail.send()
        print("Email sent successfully!")
        messages.success(request, 'Mail Sent successfully!')
        
    except Exception as e:
        print("Sorry mail was not sent.")
        print(e)
        messages.error(request, 'unable to send Mail!')
    return HttpResponseRedirect(reverse_lazy("pdata"))

####################################

def add_profile(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        form1 = UserProfile(request.POST,request.FILES)
        
        if form.is_valid() and form1.is_valid():
            # user=form.save()
            # profile=form1.save(commit=False)
            # profile.user=user
            # profile.save()
            # username = form.cleaned_data.get('username')
            # prn = form1.cleaned_data.get('prn')
            # TakeImage(username,prn)
            username = form.cleaned_data.get('username')
            prn = form1.cleaned_data.get('prn')
            TakeImage(username,prn)
            password = form.cleaned_data.get('password1')
            # user = authenticate(username = username, password = password)
            # login(request, user)
            # return HttpResponseRedirect(reverse('login'))
            # return redirect('login')
    else:
        form = SignUpForm()
        form1=UserProfile()
    return render(request, 'auth/add_profile.html', {'form': form,'form1':form1})



#############Edit Profile #############

def edit_profile(request,id):
    profile = User.objects.get(id=id)
    print(request.user.first_name)
    if request.user.first_name=="":
        print ("profile")
        form = UserProfile(instance=request.user)
    else:
        form = UserProfile(instance=request.user.userprofile)
    form1 = ProfileForm(instance=request.user)
    # messages.success(request, 'Your profile was successfully updated!')
    if request.method == 'POST':
        form1 = ProfileForm(request.POST,instance=request.user)
        if request.user.first_name == "":
            form = UserProfile(request.POST,request.FILES)
        else:
            form = UserProfile(request.POST,request.FILES,instance=request.user.userprofile)
        if form.is_valid():
            print("form")
            user=form1.save()
            profile1=form.save(commit=False)
            profile1.user=user
            profile1.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse_lazy("pdata"))
            # return redirect('pdata')
    return render(request,'auth/add_profile.html',{'form': form,'form1':form1})



