from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from doctor.models import *
from doctor.forms import *
from patient.forms import *
from patient.models import *
from builtins import Exception


def doctorlogin(request):
    return render(request,'doctor/doctorlogin.html')

def doctorregister(request):
        if request.method == 'POST':
            form1 = doctorForm(request.POST)
            if form1.is_valid():
                form1.save()
                print("succesfully saved the data")
                return render(request, 'doctor/doctorlogin.html')
                # return HttpResponse("registreration succesfully completed")
            else:
                print("form not valied")
                return HttpResponse("form not valied")
        else:
            form = doctorForm()
            return render(request, "doctor/doctorregister.html", {"form": form})


def doctordetails(request):
    qs=doctorModel.objects.all()
    return render(request,'admin/doctordetails.html',{"object":qs})

def activatedoctor(request):
    if request.method == 'GET':
        uname = request.GET.get('pid')
        print(uname)
        status = 'Activated'
        print("pid=", uname, "status=", status)
        doctorModel.objects.filter(id=uname).update(status=status)
        qs = doctorModel.objects.all()
        return render(request,"admin/doctordetails.html", {"object": qs})


def doctorlogincheck(request):
    if request.method == 'POST':
        sname = request.POST.get('email')
        print(sname)
        spasswd = request.POST.get('upasswd')
        print(spasswd)
        try:
            check = doctorModel.objects.get(email=sname,passwd=spasswd)
            # print('usid',usid,'pswd',pswd)
            print(check)
            request.session['name'] = check.name
            print("name",check.name)
            status = check.status
            print('status',status)
            if status == "Activated":
                request.session['email'] = check.email
                return render(request, 'doctor/doctopage.html')
            else:
                messages.success(request, 'doctor is not activated')
                return render(request, 'doctor/doctorlogin.html')
        except Exception as e:
            print('Exception is ',str(e))
            pass
        messages.success(request,'Invalid name and password')
        return render(request,'doctor/doctorlogin.html')

def  addtreatment(request):
    id=request.GET.get('name')
    print("id",id)
    qs=patientsympmodel.objects.filter(id=id)
    for x in qs:
        name=x.name
        symptomps=x.symptomps
        age=x.age
        famldt=x.familydata
    print("name",name,"symptomps",symptomps,"age",age,"famldata",famldt)
    obj={"name":name,"symptomps":symptomps,"age":age,"famldata":famldt}
    return render(request, 'doctor/disease-identification.html',{"object":obj})



def report(request):
    qs = {}
    chk=request.POST.get('valid')
    chk = bool(chk)
    mmse=request.POST.get('mmse')
    mmse=int(mmse)
    if mmse>=30:
        mmse=True
    else:
        mmse=False
    print(chk,"=",mmse)
    if (chk == True) and (mmse == False):
        disease='you have got alzimer-disease'
    else:
        disease='its not alzimer just less memory power'
    qs.update({"msg":disease})
    print(qs)
    return render(request,'doctor/report.html',{"qs":qs})




def doctorviewpatientdata(request):
    doctor=request.session['name']
    qs=patientsympmodel.objects.all()
    print("qs:",qs)
    return render(request,'doctor/doctorviewpatientdata.html',{"object":qs})
