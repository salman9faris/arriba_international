from django.shortcuts import render
from dashboard.models import Document, Trackingevent,Agency,Totalcount
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from home.serializer import Documentserializer,Agencyserializer, Trackingserializer,Totalcountserializer

# Create your views here.




def trackdocument(request):
    
    if request.method=="POST":
        tracking_number=request.POST.get("tracking_number")
        try:
            tracking_doc=Document.objects.get(tacking_no=tracking_number)
            if tracking_doc.tracking:
                track_event=Trackingevent.objects.filter(document=tracking_doc.id)
                context={
                    "tracks":track_event,
                    "doc":tracking_doc
                }
                return render(request,'trackdoc.html',context)
            else:
                context={
                    "error":"No Tracking document found"
                }
                return render(request,'trackdoc.html',context)
        except:
                context={
                    "error":"No Tracking document found"
                }
                return render(request,'trackdoc.html',context)
    return render(request,'home.html')



@api_view(['GET'])
def alldocapi(request):
     if request.method=='GET':
        alldoc=Document.objects.all()
        docserializer=Documentserializer(alldoc,many=True)
     return Response(docserializer.data,)

@api_view(['GET'])
def testarriba(request):
     
     return Response("working api")


@api_view(['GET'])
def docapi(request,pk):
    if request.method=='GET':
            alldoc=Document.objects.filter(id=pk)
            if alldoc:
                serializer=Documentserializer(alldoc,many=True)
                return Response({"status":200,"payload":serializer.data})
            else:
                return Response({"status":200,"message":"item not found"})

@api_view(['GET'])
def allagencyapi(request):
     if request.method=='GET':
        alllagency=Agency.objects.all()
        serializer=Agencyserializer(alllagency,many=True)
     return Response(serializer.data)

@api_view(['GET'])
def docbyagencyapi(request,pk):
    
     if request.method=='GET':
        allagency=Agency.objects.get(id=pk)
        alldoc=Document.objects.filter(agency_name=allagency.agency_name)
        serializer=Agencyserializer(alldoc,many=True)
     return Response(serializer.data)


@api_view(['GET'])
def trackingapi(request,pk):
     if request.method=='GET':
        alldoc=Document.objects.get(id=pk)
        tracking=Trackingevent.objects.filter(document=alldoc.id)
        serializer=Trackingserializer(tracking,many=True)
     return Response(serializer.data)


@api_view(['GET'])
def totaldoccount(request):
     if request.method=='GET':
        total=Totalcount.objects.all()
        serializer=Totalcountserializer(total,many=True)
     return Response(serializer.data)

@api_view(['GET'])
def refresh(request):
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
    return Response({"message":"refreshed"})