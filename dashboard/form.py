from django import forms
from .models import Document,Trackingevent,Userprofile
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  
  

class adddocForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Document
        fields = ( 'agency_name','student_name','Mobilenumber','university','submitting_for','comment')
        labels= {
            'agency_name':'Agency Name',
            "student_name":"Student Name",
            'university':'University',
            'submitting_for':'Submitting for',
            'Mobilenumber':'Mobile number',
            'comment':'Comment',
        }
        widgets={
            'agency_name':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Agency Name'
            }),
            "student_name":forms.TextInput(attrs={
                'class':'form-control','placeholder':'Student Name'
            }),
            'university':forms.TextInput(attrs={
                'class':'form-control','placeholder':'University'
            }),
            'submitting_for':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Submitting for'
            }),
            'Mobilenumber':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Mobile number'
            }),
            'comment':forms.Textarea(attrs={
                'class':'form-control','placeholder':'Comment', 'rows':"2"
            }),
           
            
        }


class TrackingForm(forms.ModelForm):
    class Meta:
        model = Trackingevent
        fields = ( 'title','comment_1','comment_2')
        labels= {
            'title':'title',
           
            'comment_1':'first event',
            'comment_2':'second event',
           
        }
        widgets={
            'title':forms.TextInput(attrs={
                'class':'form-control','placeholder':'title'
            }),
       
            'comment_1':forms.TextInput(attrs={
                'class':'form-control','placeholder':'first event'
            }),
            'comment_2':forms.TextInput(attrs={
                'class':'form-control','placeholder':'second event'
            }),


        }

        
class userprofileform(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ( 'mobile_number','email','location',"role")
        labels= {
           
            'mobile number':'mobile_number',
            'email':'email',
             'location':'location',
             "role":"role"

        }
        widgets={
            
       
            'mobile_number':forms.TextInput(attrs={
                'class':'form-control','placeholder':'mobile number'
            }),
              'email':forms.TextInput(attrs={
                'class':'form-control','placeholder':'email'
            }),
            'location':forms.TextInput(attrs={
                'class':'form-control','placeholder':'location'
            }),
             'role':forms.TextInput(attrs={
                'class':'form-control','placeholder':'role'
            }),


        }

class CustomUserCreationForm(UserCreationForm):  
    username = forms.CharField(label='username', min_length=5, max_length=150, )   
    email = forms.EmailField(label='email') 
    mobilenumber=forms.CharField(max_length=10)
    password1 = forms.CharField(label='password', widget=forms.PasswordInput,)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "name":"username",
             'class':'form-control',
             'placeholder':'username',
             'type':"text",
             'required':""

        })
        self.fields['email'].widget.attrs.update({
            "email":"email",
             'class':'form-control',
             'placeholder':'email',
             'type':"email",
             'required':""
             
        }),

        self.fields['mobilenumber'].widget.attrs.update({
                    "mobilenumber":"mobilenumber",
                    'class':'form-control',
                    'required':"",
                    'placeholder':'mobilenumber',
                    'type':"mobilenumber",
                    'maxlength':'10',
                    'minlength':'10'
                    
                }),
        self.fields['password1'].widget.attrs.update({
                        "password1":"password",
                        'class':'form-control',
                        'required':"",
                        'placeholder':'password',
                        'type':"password",
                       
                        'minlength':'6'
                        
                    }),
        self.fields['password2'].widget.attrs.update({
                        "password2":"password2",
                        'class':'form-control',
                        'required':"",
                        'placeholder':'password2',
                        'type':"password2",
                       
                        'minlength':'6'
                        
                    })
        
        labels= {
           
            'username':'username',
            'email':'email',
             'location':'location',
             "role":"role"

        }
        
    class Meta:
        model = User
        fields = ('username', 'email', 'mobilenumber', 'password1', 'password2' )
        help_texts = {
            'username': "dagdyegey",
        }
  
        widgets={
            
       
            'username':forms.TextInput(attrs={
                'class':'form-control','placeholder':'username'
            }),
              'email':forms.TextInput(attrs={
                'class':'form-control','placeholder':'email'
            }),
            'mobile_number':forms.TextInput(attrs={
                'class':'form-control','placeholder':'mobilenumber'
            }),
             'password1':forms.TextInput(attrs={
                'class':'form-control','placeholder':'password1'
            }),


            }

    def username_clean(self):  
        username = self.cleaned_data['username'].lower() 
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  
    

  