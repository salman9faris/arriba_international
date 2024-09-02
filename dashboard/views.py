from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from dashboard.decorators import unauthencticated_user,admin_only,entry_staff,associate_staff
from .form import adddocForm,TrackingForm,userprofileform
from .models import Document,Trackingevent,Agency,Country,Totalcount,Userprofile
import random,datetime,calendar,string
from django.db.models import Count
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms  
from django.shortcuts import redirect, render  
from django.contrib import messages  
from .form import CustomUserCreationForm 




@login_required(login_url="loginuser")
@entry_staff
def dashboard(request):
    agency=Agency.objects.all().order_by("-updated_date")
    total=Totalcount.objects.all()
    country_count=Document.objects.values("submitting_for").order_by("submitting_for").annotate(count=Count("submitting_for"))
    context={
        "agencies":agency,
        "total_count":total,
        "country_count":country_count
    }
    return render(request,"index.html",context)

@login_required(login_url="loginuser")
@entry_staff
def refreshdoc(request):
    closeddoc=Document.objects.filter(status="closed").__len__()
    openeddoc=Document.objects.filter(status="open").__len__()
    processingdoc=Document.objects.filter(status="processing").__len__()
    total_count=Totalcount.objects.get()
    total_count.opened_doc=openeddoc
    total_count.closed_doc=closeddoc
    total_count.processing=processingdoc
    total_count.total_doc=openeddoc+closeddoc+processingdoc
    total_count.save()
    total=Totalcount.objects.all()
    country_count=Document.objects.values("submitting_for").order_by("submitting_for").annotate(count=Count("submitting_for"))
    agency_count=Document.objects.values("agency_name").order_by("agency_name").annotate(count=Count("status"))
   
    for agency_count in agency_count:
        try:
            agency=Agency.objects.get(agency_name=agency_count["agency_name"])
            agency.total_doc=agency_count["count"]
            agency.save()
           
        except:
            agency=Agency(agency_name=agency_count["agency_name"],total_doc=agency_count["count"])
          
            agency.save()
    agencies=Agency.objects.all().order_by("-updated_date")
    context={
        "agencies":agencies,
        "total_count":total,
        "country_count":country_count
    }
    return render(request,"index.html",context)



@login_required(login_url="loginuser")
@entry_staff
def adddocument(request):
    value="add document details"
    if request.method=="POST":
        form=adddocForm(request.POST)
        if form.is_valid():
            document=form.save(commit=False)
            document.agency_name=document.agency_name.lower()
            document.university=document.university.lower()
            document.submitting_for=document.submitting_for.lower()
            date=datetime.date.today()
            document.tacking_no=calendar.month_name[date.month][0:3]+str(random.randint(1200,9500))+random.choice(string.ascii_letters)+str(date.day)
            agency,created=Agency.objects.get_or_create(agency_name=document.agency_name.lower())
            agency.total_doc+=1
            agency.opened_doc+=1
            agency.save()
            document.save()
            return render(request,"new_document.html")
    form=adddocForm
    context={
        'form':form,
         "value":value,
    }
    return render(request,"new_document.html",context)

@login_required(login_url="loginuser")
@associate_staff
def updatedocument(request,pk):
    value="update details"
    event=get_object_or_404(Document,id=pk)
    try:
        agent=Agency.objects.get(agency_name=event.agency_name)
        agent.total_doc-=1
        agent.save()
    except:
        pass
    form=adddocForm(request.POST or None,instance=event)
    if form.is_valid():
        document=form.save(commit=False)
        document.agency_name=document.agency_name.lower()
        document.university=document.university.lower()
        document.submitting_for=document.submitting_for.lower()
        agency,created=Agency.objects.get_or_create(agency_name=document.agency_name.lower())
        agency.save()
        document.save()
        return redirect("detaildocument",pk)
    
    context={
        'form':form,
         "value":value,
    }
    return render(request,"new_document.html",context)


@login_required(login_url="loginuser")
@entry_staff
def showdocument(request):
    opendoc=Document.objects.filter(status="open").order_by('-created_date')
    closeddoc=Document.objects.filter(status="closed").order_by('-created_date')
    processingddoc=Document.objects.filter(status="processing").order_by('-created_date')
    context={
        "opendoc":opendoc,
        "closeddoc":closeddoc,
        "processingddoc":processingddoc
    }
    return render(request,"show_document.html",context)

@login_required(login_url="loginuser")
@entry_staff
def detaildocument(request,pk):
    doc=Document.objects.get(id=pk)
    tracks=Trackingevent.objects.filter(document=doc).order_by('-date')
    context={
        "filter":"none",
        "doc":doc,
        "tracks":tracks
    }
    return render(request,"document_details.html",context)

@login_required(login_url="loginuser")
@entry_staff
def addevent(request,pk):
    value="tracking details"
    if request.method=="POST":
        doc=Document.objects.get(id=pk)
        form=TrackingForm(request.POST)
        if form.is_valid():
            trackevent=form.save(commit=False)
            trackevent.document=doc
            trackevent.save()
            return redirect("detaildocument",pk=pk)
    form=TrackingForm
    context={
        'form':form,
        "value":value,

    }
    return render(request,"new_document.html",context)


@login_required(login_url="loginuser")
@associate_staff
def updatetrackevent(request,pk):
    value="update tracking details"
    event=get_object_or_404(Trackingevent,id=pk)
    form=TrackingForm(request.POST or None,instance=event)
    id=event.document.id
    if form.is_valid():
        form.save()
        return redirect("detaildocument",pk=id)
    context={
        'form':form, "value":value,
    }
    return render(request,"new_document.html",context)

@login_required(login_url="loginuser")
@admin_only
def deletetrackevent(request,pk):
    try:
        event=Trackingevent.objects.filter(document=pk)
        event.delete()
        
        return redirect("detaildocument",pk=pk)
    except:
        return redirect("detaildocument",pk=id)
 
  

@login_required(login_url="loginuser")
@entry_staff
def docbyagency(request,pk):
    opendoc=Document.objects.filter(status="open",agency_name=pk).order_by('-created_date')
    closeddoc=Document.objects.filter(status="closed",agency_name=pk).order_by('-created_date')
    processingddoc=Document.objects.filter(status="processing",agency_name=pk).order_by('-created_date')
    processing_count=processingddoc.count()
    opendoc_count=opendoc.count()
    totaldoc_count=opendoc_count+closeddoc.count()+processing_count
    filterby="agency"
    value=pk
    context={
        "filterby":filterby,
        "value":value,
        "opendoc_count":opendoc_count,
        "processin_count":processing_count,
        "totaldoc_count":totaldoc_count,
        "opendoc":opendoc,
        "closeddoc":closeddoc,
        "processingddoc":processingddoc
    }
    
    return render(request,"show_document.html",context)


@login_required(login_url="loginuser")
@entry_staff
def docbycountry(request,pk):
    filterby="country"
    value=pk
    opendoc=Document.objects.filter(status="open",submitting_for=pk.lower()).order_by('-created_date')
    closeddoc=Document.objects.filter(status="closed",submitting_for=pk.lower()).order_by('-created_date')
    processingddoc=Document.objects.filter(status="processing",submitting_for=pk.lower()).order_by('-created_date')
    processing_count=processingddoc.count()
    opendoc_count=opendoc.count()
    totaldoc_count=opendoc_count+closeddoc.count()+processing_count
    context={
         "filterby":filterby,
         "value":value,
          "opendoc_count":opendoc_count,
        "processin_count":processing_count,
        "totaldoc_count":totaldoc_count,
        "opendoc":opendoc,
        "closeddoc":closeddoc,
        "processingddoc":processingddoc
    }
    
    return render(request,"show_document.html",context)



@login_required(login_url="loginuser")
@admin_only
def updateclosed(request,pk):
    doc=Document.objects.get(id=pk)
    doc.tracking="False"
    doc.status="closed"
    doc.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url="loginuser")
@entry_staff
def updateopen(request,pk):
    doc=Document.objects.get(id=pk)
    doc.status="open"
    doc.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url="loginuser")
@entry_staff
def updateprocessing(request,pk):
    doc=Document.objects.get(id=pk)
    doc.status="processing"
    doc.save()
    return redirect(request.META['HTTP_REFERER'])



def loginuser(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password= request.POST.get("password")
        try:
            user=User.objects.get(username=username)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "username or password doesnt match")
        except:
            
            messages.error(request,"user not found")
    return render(request,"login.html")



def registeruser(request):  
    args={}
    form = CustomUserCreationForm(request.POST)  
    if request.method=='POST':
        form = CustomUserCreationForm(request.POST) 
        try:
            if form.is_valid():
                mobile_number=form.cleaned_data['mobilenumber']
                password1=form.cleaned_data['password1']
                password2=form.cleaned_data['password2']
                user=form.save()
                group=Group.objects.get(name="admin") 
                user.groups.add(group)
                employee_id=str(random.randint(12000,95000))
                profile,created=Userprofile.objects.get_or_create(name=user,employeeid=employee_id,
                                                                email=user.email,mobile_number=mobile_number,group="admin")
                profile.save()
                login(request,user)
                return redirect("profile")
            
        except:
            messages.error(request,"someting went wrong")
           
     
            
    args['form'] = form
    
    return render(request,"register.html",args)




def logoutuser(request):
    logout(request)
    return render(request,"login.html")

def profile(request):
    userdetails=None
    your_details=Userprofile.objects.get(name=request.user)
    employee_details=Userprofile.objects.exclude(name=your_details.name).order_by("-created_date")
    context={"userdetails":your_details,
             "employee_details":employee_details
             }
    return render(request,"userdetails.html",context)



@login_required(login_url="loginuser")
@admin_only
def edituserprofile(request,pk):
    value="update user details"
    event=get_object_or_404(Userprofile,id=pk)
    
    form=userprofileform(request.POST or None,instance=event)
    if form.is_valid():
        form.save()
        return redirect("profile")
    context={
        'form':form, "value":value,
    }
    return render(request,"new_document.html",context)


@login_required(login_url="loginuser")
@admin_only
def updategroupadmin(request,pk):
    usergroup=Userprofile.objects.get(id=pk)
    currentgroupname=usergroup.group
    usergroup.group='admin'
    usergroup.save()
    currentgroup = Group.objects.get(name=currentgroupname)
    currentgroup.user_set.remove(usergroup.name)
    group = Group.objects.get(name="admin")
    group.user_set.add(usergroup.name)
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url="loginuser")
@admin_only
def updategroupsassociate(request,pk):
    
    usergroup=Userprofile.objects.get(id=pk)
    currentgroupname=usergroup.group
    usergroup.group='associate'
    currentgroup = Group.objects.get(name=currentgroupname)
    currentgroup.user_set.remove(usergroup.name)
    group = Group.objects.get(name="associate")
    group.user_set.add(usergroup.name)
    usergroup.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url="loginuser")
@admin_only
def updategroupstaff(request,pk):
   
    usergroup=Userprofile.objects.get(id=pk)
    currentgroupname=usergroup.group
    usergroup.group='staff'
    usergroup.save()
    currentgroup = Group.objects.get(name=currentgroupname)
    currentgroup.user_set.remove(usergroup.name)
    group = Group.objects.get(name="staff")
    group.user_set.add(usergroup.name)
    return redirect(request.META['HTTP_REFERER'])




@login_required(login_url="loginuser")
@admin_only
def updategroupfresher(request,pk): 
    usergroup=Userprofile.objects.get(id=pk)
    currentgroupname=usergroup.group
    usergroup.group='fresher'
    usergroup.save()
    currentgroup = Group.objects.get(name=currentgroupname)
    currentgroup.user_set.remove(usergroup.name)
    group = Group.objects.get(name="fresher")
    group.user_set.add(usergroup.name)
    
    return redirect(request.META['HTTP_REFERER'])