from rest_framework import serializers
from dashboard.models import Document,Agency,Trackingevent,Totalcount,Userprofile
from django.contrib.auth.models import User,Group

class Documentserializer(serializers.ModelSerializer):
    class Meta:
        model=Document
        fields='__all__'
        depth=1


class Agencyserializer(serializers.ModelSerializer):
    class Meta:
        model=Agency
        fields='__all__'


class Trackingserializer(serializers.ModelSerializer):
    class Meta:
        model=Trackingevent
        fields='__all__'

class Totalcountserializer(serializers.ModelSerializer):
    class Meta:
        model=Totalcount
        fields='__all__'

class userserializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        depth=2
        fields=["id","username","first_name","last_name"]


class Userprofileserializer(serializers.ModelSerializer):
    name=userserializer()
    class Meta:
        model=Userprofile
        depth=2
        fields=["id","employeeid","email","name","location","role","mobile_number"]
        