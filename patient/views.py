from django.shortcuts import render
from patient.forms import *
from django.http import HttpResponse

from builtins import Exception
from django.contrib import messages




def patientlogin(request):
    return render(request,'patient/patientlogin.html')


def patientregister(request):
        if request.method == 'POST':
            form=patientForm(request.POST)
            if form.is_valid():
                form.save()
                print("succesfully saved the data")
                return render(request, 'patient/patientlogin.html')
            else:
                print("form not valied")
                return HttpResponse("form not valied")
        else:
            form=patientForm()
            return render(request, "patient/patientregister.html", {"form":form})




def patientlogincheck(request):
    if request.method == 'POST':
        sname = request.POST.get('email')
        print(sname)
        spasswd = request.POST.get('upasswd')
        print(spasswd)
        try:
            check = patientModel.objects.get(email=sname,passwd=spasswd)
            # print('usid',usid,'pswd',pswd)
            print(check)
            request.session['name'] = check.name
            print("name",check.name)
            status = check.status
            print('status',status)
            if status == "Activated":
                request.session['email'] = check.email
                return render(request, 'patient/patientpage.html')
            else:
                messages.success(request, 'patient is not activated')
                return render(request, 'patient/patientlogin.html')
        except Exception as e:
            print('Exception is ',str(e))
            pass
        messages.success(request,'Invalid name and password')
        return render(request,'patient/patientlogin.html')

def patientdetails(request):
    qs=patientModel.objects.all()
    return render(request,'admin/patientdetails.html',{"object":qs})


def patntsymptms(request):
    name=request.POST.get('name')
    age=request.POST.get('age')
    mble=request.POST.get('mobile')
    gndr=request.POST.get('gndr')
    famly=request.POST.get('famly')
    symp=request.POST.get('symp')
    patientsympmodel.objects.create(name=name,age=age,mobileno=mble,gender=gndr,familydata=famly,symptomps=symp)
    return render(request,'patient/patientsymptoms.html')



def patientsymptoms(request):
    return render(request,'patient/patientsymptoms.html')