from rest_framework import serializers
from dashboard.models import Document,Agency,Trackingevent,Totalcount

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
        