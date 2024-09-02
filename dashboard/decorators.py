from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render  


def unauthencticated_user(view_func):
    def wrapper_fun(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        else:
            print("done_decoratoor3")
            return view_func(request,*args,**kwargs)
    return wrapper_fun



def admin_only(view_func):
    def wrapper_fun(request,*args,**kwargs):
        group:None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=="associate":
           return render(request,"error_page.html")
        if group=='admin':
            return view_func(request,*args,**kwargs)
        else:
            return render(request,"error_page.html")
    return wrapper_fun

def associate_staff(view_func):
    def wrapper_fun(request,*args,**kwargs):
        group:None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=="associate":
           return view_func(request,*args,**kwargs)
        if group=='admin':
            return view_func(request,*args,**kwargs)
        else:
            return render(request,"error_page.html")
    return wrapper_fun

def entry_staff(view_func):
    def wrapper_fun(request,*args,**kwargs):
        group:None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=="staff":
           return view_func(request,*args,**kwargs)
        if group=='admin':
          
            return view_func(request,*args,**kwargs)
        if group=='associate':
           
            return view_func(request,*args,**kwargs)
        else:
            return render(request,"error_page.html")
    return wrapper_fun


def beginner(view_func):
    def wrapper_fun(request,*args,**kwargs):
        group:None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=="fresher":
           return view_func(request,*args,**kwargs)
        else:
            return render(request,"error_page.html")
    return wrapper_fun