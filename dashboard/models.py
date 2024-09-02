from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    agency_name=models.CharField(max_length=256,blank=False)
    student_name=models.CharField(max_length=256,blank=False)
    Mobilenumber=models.CharField(max_length=50,blank=False)
    university=models.CharField(max_length=256,blank=True)
    submitting_for=models.CharField(max_length=256,blank=True)
    tacking_no=models.CharField(max_length=25,blank=False,unique=True)
    tracking=models.BooleanField(default=True,blank=False)
    created_date=models.DateTimeField(auto_now_add=True,)
    comment=models.CharField(max_length=256,blank=False)
    status=models.CharField(max_length=25,blank=False,default="open")

    def __str__(self) -> str:
        return str(self.id)
    

  
    

class Trackingevent(models.Model):
    id = models.AutoField(primary_key=True)
    document=models.ForeignKey(Document,on_delete=models.CASCADE)
    title=models.CharField(max_length=256)
    date=models.DateTimeField(auto_now_add=True,)
    comment_1=models.CharField(max_length=256,blank=True)
    comment_2=models.CharField(max_length=256,blank=True)

class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    agency_name=models.CharField(max_length=256,blank=False,)
    Mobilenumber=models.CharField(max_length=50,blank=True,null=True)
    total_doc=models.PositiveIntegerField(blank=True,null=True,default=0)
    opened_doc=models.PositiveIntegerField(blank=True,null=True,default=0)
    created_date=models.DateTimeField(auto_now_add=True,)
    updated_date=models.DateTimeField(auto_now= True,blank=True,null=True)

    


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country=models.CharField(max_length=256,blank=False)
    number_doc=models.PositiveIntegerField(blank=True,null=True,default=0)

class Totalcount(models.Model):
    id = models.AutoField(primary_key=True)
    total_doc=models.PositiveIntegerField(blank=False,default=0)
    opened_doc=models.PositiveIntegerField(blank=False,default=0)
    processing=models.PositiveIntegerField(blank=False,default=0)
    closed_doc=models.PositiveIntegerField(blank=True,null=True,default=0)
   
    
class Userprofile(models.Model):
    id = models.AutoField(primary_key=True)
    employeeid=models.PositiveIntegerField()
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile_number=models.CharField("Mobile number",max_length=80,blank=True)
    email=models.CharField("email id",max_length=256,blank=True)
    role=models.CharField(max_length=25,blank=True)
    location=models.CharField(max_length=64,blank=True)
    group=models.CharField(max_length=24)
    created_date=models.DateTimeField(auto_now_add=True,)

    def __str__(self) -> str:
        return str(self.name)
    