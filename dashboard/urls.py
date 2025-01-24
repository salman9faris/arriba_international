

from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     
     path("dashboard-user",views.dashboard,name='dashboard'),
     path("refresh",views.refreshdoc,name='refreshdoc'),
     path("new",views.adddocument,name='adddocument'),
     path("document",views.showdocument,name='showdocument'),
     path("alldocument/<int:pk>",views.showalldocument,name='showalldocument'),
     path("topdocument",views.topagency,name='topdocument'),

     path("topdocumentcountry",views.topcountry,name='topdocumentcountry'),
     path("docbyagency/<str:pk>",views.docbyagency,name='docbyagency'),
     path("docbycountry/<str:pk>",views.docbycountry,name='docbycountry'),
     path("addagencydetails/<int:pk>",views.addagencydetails,name='addagencydetails'),

     path("details/<int:pk>",views.detaildocument,name='detaildocument'),

     path("updateclosed/<int:pk>",views.updateclosed,name='updateclosed'),
     path("updateopen/<int:pk>",views.updateopen,name='updateopen'),
     path("updateprocessing/<int:pk>",views.updateprocessing,name='updateprocessing'),

     path("addevent/<int:pk>",views.addevent,name='addevent'),
     path("updatetrackevent/<int:pk>",views.updatetrackevent,name='updatetrackevent'),
     path("deletetrackevent/<int:pk>",views.deletetrackevent,name='deletetrackevent'),

     path("updatedocument/<int:pk>",views.updatedocument,name='updatedocument'),

     path("login",views.loginuser,name='loginuser'),
     path("register",views.registeruser,name='registeruser'),
     path("logoutuser",views.logoutuser,name='logoutuser'),
     path("profile",views.profile,name='profile'),
     path("editprofile/<int:pk>",views.edituserprofile,name='edituserprofile'),

     path("admin/<int:pk>",views.updategroupadmin,name='updategroupadmin'),
     path("associate/<int:pk>",views.updategroupsassociate,name='updategroupsassociate'),
     path("staff/<int:pk>",views.updategroupstaff,name='updategroupstaff'),
     path("entry/<int:pk>",views.updategroupfresher,name='updategroupfresher'),

     path("invoice",views.showinvoice,name='showinvoice'),
     path("viewinvoice/<int:pk>",views.viewinvoice,name='viewinvoice'),

      path("refreshinvoice",views.refreshinvoice,name='refreshinvoice'),

     path("addinvoice/<int:pk>",views.addinvoice,name='addinvoice'),
     path("updateinvoice/<int:pk>",views.updateinvoice,name='updateinvoice'),
     path("deleteinvoice/<int:pk>",views.deleteinvoice,name='deleteinvoice'),

     

     
]