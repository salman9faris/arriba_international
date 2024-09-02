from django.contrib import admin

from dashboard.models import Document,Trackingevent,Agency,Country,Totalcount,Userprofile

# Register your models here.
class Agencytadmin(admin.ModelAdmin):
    list_display=("id","agency_name","Mobilenumber","total_doc","opened_doc","created_date","updated_date")

class Documentadmin(admin.ModelAdmin):
    list_display=("id","agency_name","student_name","Mobilenumber","university","submitting_for","tacking_no","tracking","status","created_date","comment")

class Trackingeventadmin(admin.ModelAdmin):
    list_display=("id","document","title","date","comment_1","comment_2")
class Countryadmin(admin.ModelAdmin):
     list_display=("id","country","number_doc")

class Totalcountadmin(admin.ModelAdmin):
     list_display=("id","total_doc","opened_doc","processing","closed_doc")

class Userprofileadmin(admin.ModelAdmin):
     list_display=("id","employeeid","name","mobile_number","email","role","location",)

                  
# Register your models here.

admin.site.register(Agency,Agencytadmin),
admin.site.register(Document,Documentadmin),
admin.site.register(Trackingevent,Trackingeventadmin)
admin.site.register(Country,Countryadmin),
admin.site.register(Totalcount,Totalcountadmin),
admin.site.register(Userprofile,Userprofileadmin),