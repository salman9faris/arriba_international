from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from dashboard.decorators import unauthencticated_user,admin_only,entry_staff,associate_staff
from .form import adddocForm,TrackingForm,userprofileform,Agencydetailsform
from .models import Country, Document,Trackingevent,Agency,Totalcount,Userprofile,Invoicedetails
import random,datetime,calendar,string
from django.db.models import Count,Q
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms  
from django.shortcuts import redirect, render  
from django.contrib import messages  
from .form import CustomUserCreationForm ,Addinvoiceform
import random
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse





@login_required(login_url="loginuser")
@entry_staff
def dashboard(request):
    now = timezone.now()
    agency=Agency.objects.all().order_by("-total_doc")[:5]
    total=Totalcount.objects.all()
    country=Country.objects.all().order_by("-total_doc")[:5]
    agencycount=Agency.objects.count()
    countrycount=Country.objects.count()
    todaycount = Document.objects.filter(created_date=now.date()).count()
    context={
        "agencies":agency,
        "total_count":total,
        "country":country,
        "countrycount":countrycount,
        "agencycount":agencycount,
        "todaycount":todaycount

    }
    return render(request,"index.html",context)

@login_required(login_url="loginuser")
@entry_staff
def refreshdoc(request):
    now = timezone.now()
    status_counts = Document.objects.values('status') \
    .annotate(count=Count('status')) \
    .order_by('status')
    total_count=Totalcount.objects.get()
    total_count.opened_doc=status_counts[1]['count']
    total_count.closed_doc=status_counts[0]['count']
    total_count.processing=status_counts[2]['count']
    total_count.total_doc=status_counts[0]['count']+status_counts[1]['count']+status_counts[2]['count']
    total_count.save()
    Agency.objects.all().update(total_doc=0,opened_doc=0)
    
    country_count= Document.objects.values('submitting_for') \
    .annotate(open=Count('status', filter=Q(status='open')), processing=Count('status', filter=Q(status='processing')),
              closed=Count('status', filter=Q(status='closed'))) \
    .order_by('submitting_for')
    agency_count= Document.objects.values('agency_name') \
    .annotate(open=Count('status', filter=Q(status='open')), processing=Count('status', filter=Q(status='processing')),
              closed=Count('status', filter=Q(status='closed'))) \
    .order_by('agency_name')
    for agency_count in agency_count:
        try:
            agency=Agency.objects.get(agency_name=agency_count["agency_name"])
            agency.opened_doc= agency_count["open"]+agency_count["processing"]
            agency.total_doc=agency_count["open"]+agency_count["processing"]+agency_count["closed"]
            agency.save()
        except:
            agency=Agency(agency_name=agency_count["agency_name"],
                          opened_doc= agency_count["open"]+agency_count["processing"],
                          total_doc=agency_count["open"]+agency_count["processing"]+agency_count["closed"])
            agency.save()
    for country_count in country_count:
        try:
         
            country=Country.objects.get(country=country_count["submitting_for"])
            country.opened_doc= country_count["open"]+country_count["processing"]
            country.total_doc=country_count["open"]+country_count["processing"]+country_count["closed"]
            country.save()
        except:
            country=Country(
                  country=country_count["submitting_for"],
                  opened_doc= country_count["open"]+country_count["processing"],
                  total_doc=country_count["open"]+country_count["processing"]+country_count["closed"]
            )
            country.save()
    country=Country.objects.all().order_by("-total_doc")[:5]
    agencies=Agency.objects.all().order_by("-total_doc")[:5]
    total=Totalcount.objects.all()
    agencycount=Agency.objects.count()
    countrycount=Country.objects.count()
    todaycount = Document.objects.filter(created_date=now.date()).count()
    context={
        "agencies":agencies,
        "total_count":total,
        "country":country,
       
        "agencycount":agencycount ,
          "countrycount":countrycount,
           "todaycount":todaycount

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
    opendoc=Document.objects.filter(status="open").order_by('-created_date')[:10]
    processingddoc=Document.objects.filter(status="processing").order_by('-created_date')[:5]
    closeddoc=Document.objects.filter(status="closed").order_by('-created_date')[:5]
    context={
        "opendoc":opendoc,
        "closeddoc":closeddoc,
        "processingddoc":processingddoc
    }
    return render(request,"show_document.html",context)

@login_required(login_url="loginuser")
@entry_staff
def showalldocument(request,pk):
    if pk==0:
        opendoc=Document.objects.filter(status="open").order_by('-created_date')
        processingddoc=None
        closeddoc=None
    elif pk==1:
        processingddoc=Document.objects.filter(status="processing").order_by('-created_date')
        opendoc=None
        closeddoc=None
    else:
        closeddoc=Document.objects.filter(status="closed").order_by('-created_date')
        processingddoc=None
        opendoc=None
    context={
        "opendoc":opendoc,
        "closeddoc":closeddoc,
        "processingddoc":processingddoc
    }
    return render(request,"show_document.html",context)




def topagency(request):
    agency=Agency.objects.all().order_by("-updated_date")
    title="Agency"
    context={
        "agencies":agency,
        "title":title
       
       
    }
    return render(request,"topdocument.html",context)


def topcountry(request):
    country=Country.objects.all().order_by("-total_doc")
    title="Submitting for"
    context={
        "country":country,
        "title":title
       
    }
    return render(request,"topdocument.html",context)






@login_required(login_url="loginuser")
@entry_staff
def detaildocument(request,pk):
    doc=Document.objects.get(id=pk)
    invoice=Invoicedetails.objects.filter(document=doc).order_by('-billing_date')
    tracks=Trackingevent.objects.filter(document=doc).order_by('-date')
    context={
        "filter":"none",
        "doc":doc,
        "tracks":tracks,
        "invoices":invoice
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
        "value":value,    }
    return render(request,"new_document.html",context)

@login_required(login_url="loginuser")
@entry_staff
def addagencydetails(request,pk):
    value="Agency details"
    if request.method=="POST":
        agnecy=get_object_or_404(Agency,id=pk)
       
        form=Agencydetailsform(request.POST)
        form=Agencydetailsform(request.POST or None,instance=agnecy)
       
        if form.is_valid():
            agencydetails=form.save(commit=False)
           
            agencydetails.save()
            return redirect("docbyagency",pk=agnecy.agency_name)
    form=Agencydetailsform
    context={
        'form':form,
        "value":value,    }
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
@admin_only
def showinvoice(request):
    pendinginvoice=Invoicedetails.objects.all().order_by('-created_date')
    closedinvoice=Invoicedetails.objects.all().order_by('-created_date')
   
   
    context={
       "paid":"N/A",
       "balance":"N/A",
       "total":"N/A",
        "pendinginvoices":pendinginvoice,
        "closedinvoices":closedinvoice
    }
    return render(request,"showallinvoice.html",context)



@login_required(login_url="loginuser")
@admin_only
def viewinvoice(request,pk):
    invoice=Invoicedetails.objects.get(id=pk)
    doc=invoice.document.id
    context={
       "invoice":invoice,
       "doc":doc
    }
    return render(request,"invoice.html",context)

@login_required(login_url="loginuser")
@admin_only
def refreshinvoice(request):
    pendinginvoice=Invoicedetails.objects.all().order_by('-created_date')
    closedinvoice=Invoicedetails.objects.all().order_by('-created_date')
    paid=Invoicedetails.objects.aggregate(Sum('paid'))
    balance=Invoicedetails.objects.aggregate(Sum('balance'))
    total=Invoicedetails.objects.aggregate(Sum('total'))
    context={
       "paid":paid['paid__sum'],
       "balance":balance['balance__sum'],
       "total":total['total__sum'],
        "pendinginvoices":pendinginvoice,
        "closedinvoices":closedinvoice
    }
    return render(request,"showinvoice.html",context)


@login_required(login_url="loginuser")
@associate_staff
def addinvoice(request,pk):
    value="Add Bills"
    if request.method=="POST":
        doc=Document.objects.get(id=pk)
        form=Addinvoiceform(request.POST)
      
        if form.is_valid():
            addinvoice=form.save(commit=False)
            price=form.cleaned_data['price']
            quanity=form.cleaned_data['quantity']
            paid=form.cleaned_data['paid']
            total=price*quanity
            addinvoice.document=doc
            random_number=random.randint(111211,992123)
            unique=Invoicedetails.objects.filter(invoice_number=random_number)
            while  len(unique)>0:
                random_number=random.randint(111211,919321)
                unique=Invoicedetails.objects.filter(invoice_number=random_number) 
            addinvoice.invoice_number=random_number
            print(f'pay status-----{form.cleaned_data['payment_status']}')
            doc.pay_status=form.cleaned_data['payment_status']

            doc.save()
            addinvoice.total=total
            addinvoice.balance=total-paid
            addinvoice.save()
            
            return redirect("detaildocument",pk=pk)
    form=Addinvoiceform
    context={
        'form':form,
        "value":value,
    }
    return render(request,"new_document.html",context)



@login_required(login_url="loginuser")
@associate_staff
def updateinvoice(request,pk):
    value="update Invoice"
   
    event=get_object_or_404(Invoicedetails,id=pk)
    
    form=Addinvoiceform(request.POST or None,instance=event)
    id=event.document.id
    
    if form.is_valid():
            doc=Document.objects.get(id=id)
            addinvoice=form.save(commit=False)
            price=form.cleaned_data['price']
            quanity=form.cleaned_data['quantity']
            paid=form.cleaned_data['paid']
            total=price*quanity
            doc.pay_status=form.cleaned_data['payment_status']

            doc.save()
            addinvoice.total=total
            addinvoice.balance=total-paid
            addinvoice.save()
            return redirect("detaildocument",pk=id)
    context={
        'form':form, "value":value,
    }
    return render(request,"new_document.html",context)

@login_required(login_url="loginuser")
@admin_only
def deleteinvoice(request,pk):  
    event=Invoicedetails.objects.get(id=pk)
    doc=event.document.id
    try:
        event=Invoicedetails.objects.filter(id=pk)
        
        event.delete()
        
        return redirect("detaildocument",pk=doc)
    except:
        return redirect("detaildocument",pk=doc)
    







@login_required(login_url="loginuser")
@entry_staff
def docbyagency(request,pk):
    opendoc=Document.objects.filter(status="open",agency_name=pk).order_by('-created_date')
    closeddoc=Document.objects.filter(status="closed",agency_name=pk).order_by('-created_date')
    processingddoc=Document.objects.filter(status="processing",agency_name=pk).order_by('-created_date')
    agency=Agency.objects.get(agency_name=pk)
    
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
        "processingddoc":processingddoc,
        "agency":agency
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
    doc.tracking="True"
    doc.status="open"
    doc.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url="loginuser")
@entry_staff
def updateprocessing(request,pk):
    doc=Document.objects.get(id=pk)
    doc.tracking="True"
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
        groups=["admin","associate","staff","fresher"]
        form = CustomUserCreationForm(request.POST)
        for group in groups:
            group_item,created=Group.objects.get_or_create(name=group)
            group_item.save()
        try:
            if form.is_valid():
                mobile_number=form.cleaned_data['mobilenumber']
                password1=form.cleaned_data['password1']
                password2=form.cleaned_data['password2']
                
                if Group.objects.get(name="fresher"):
                    user=form.save()
                    group=Group.objects.get(name="fresher") 
                    user.groups.add(group)
                    employee_id=str(random.randint(12000,95000))
                    profile,created=Userprofile.objects.get_or_create(name=user,employeeid=employee_id,
                                                                    email=user.email,mobile_number=mobile_number,group="fresher")
                    profile.save()
                    login(request,user)
                    return redirect("profile")
                else:
                    args['form'] = form
                    return render(request,"register.html",args)
                
            
        except:
            messages.error(request,"contact admin")
            print(messages)
            args['form'] = form
            return render(request,"register.html",args)
     
            
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