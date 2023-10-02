from django import forms
from django.contrib.auth.views import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.utils.translation import gettext,gettext_lazy as _
from .models import Post
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()
class Signupform(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(render_value = True,attrs={'class':'form-control','placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='Confirm Password(again)',widget=forms.PasswordInput(render_value = True,attrs={'class':'form-control','placeholder': 'Enter your confirm password'}))
        
    class Meta:
        model=User
        fields=['first_name','last_name','email','date_of_birth','street_address','city_name','state_name','zip_code','phone_number','gender']
        labels={
            'first_name':'FirstName',
            'last_name':'LastName',
            'email':'Email',
        }
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'},),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your last name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}),
            # 'date_of_birth':forms.TextInput(attrs={'class':'form-control'}),
            'street_address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your address'}),
            'city_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your city'}),
            'state_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your state'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your zip-code'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your phone number'}),
            'date_of_birth':forms.DateTimeInput(attrs={'class':'form-control','placeholder':'MM/DD/YY'}),
            'gender':forms.Select(),
            # 'bio':forms.Textarea(attrs={'class':'form-control'}),
            # 'link':forms.TextInput(attrs={'class':'form-control'}),
        }
    def clean_first_name(self):
        value = self.cleaned_data['first_name']
        if value=='': 
            raise forms.ValidationError("Please Enter Your name")
        return value

    def clean_last_name(self):
        value = self.cleaned_data['last_name']
        if value=='': 
            raise forms.ValidationError("Please Enter Your last name")
        return value
    
    def clean_email(self):
        value = self.cleaned_data['email']
        if value=='': 
            raise forms.ValidationError("email is not valid.")
        return value
    
    def clean_street_address(self):
        value = self.cleaned_data['street_address']
        if value=='': 
            raise forms.ValidationError("Please Enter Your Address")
        return value


    def clean_city_name(self):
        value = self.cleaned_data['city_name']
        if value=='': 
            raise forms.ValidationError("Please Enter Your City Name")
        return value
    
    def clean_state_name(self):
        value = self.cleaned_data['state_name']
        if value=='': 
            raise forms.ValidationError("Please Enter State Name")
        return value
    
    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        if value.isdigit()==False:
            raise forms.ValidationError("Only digit allows.")
        if value=='': 
            raise forms.ValidationError("Please Enter Your phone Number")
        
        if len(value) < 10:
            raise forms.ValidationError("Please Enter Your phone Number")
        return value
    
    def clean_zip_code(self):
        value = self.cleaned_data['zip_code']
        if value.isdigit()==False:
            raise forms.ValidationError("Only digit allows.")
        if value=='': 
            raise forms.ValidationError("Please Enter Your 6 Digit zip_code")
        
        if len(value) < 6:
            raise forms.ValidationError("Please Enter Your 6 Digit zip_code")
        return value

      
        


class loginform(AuthenticationForm):
   username=UsernameField(widget=forms.EmailInput(attrs={'autofocus':True,'class':'form-control'}))
   password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(render_value = True,attrs={'autocomplete':'current-password','class':'form-control'}))
   

class Postform(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(Postform, self).__init__(*args, **kwargs)
    #     self.fields['author'].widget.attrs['readonly'] = True
    class Meta:
        model=Post
        fields=['title','desc']
        labels={'title':'Title',
                'desc':'Description'}
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'desc':forms.Textarea(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'class':'form-control'}),

        }
    def clean_title(self):
        # title = self.cleaned_data['title']
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title

    def clean_desc(self):
        desc = self.cleaned_data['desc']
        if  len(desc) < 5:
            raise forms.ValidationError('Please Fill this fields.')
        return desc


class Updateprofile(forms.ModelForm,):
   
    class Meta:
        model=User
        
        fields=['first_name','last_name','email','date_of_birth','street_address','city_name','state_name','zip_code','phone_number','gender','bio','link']
        labels={
            'first_name':'FirstName',
            'last_name':'LastName',
            'email':'Email',
        }
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'},),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            # 'date_of_birth':forms.TextInput(attrs={'class':'form-control'}),
            'street_address':forms.TextInput(attrs={'class':'form-control'}),
            'city_name':forms.TextInput(attrs={'class':'form-control'}),
            'state_name':forms.TextInput(attrs={'class':'form-control'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'class':'form-control'}),
            'gender':forms.Select(),
            'bio':forms.Textarea(attrs={'class':'form-control'}),
            'link':forms.TextInput(attrs={'class':'form-control'}),
        }
        # # error_messages={
        # #     'email':{'required':'Please Enter Your Email'}
        # # }
    def clean_first_name(self):
        value = self.cleaned_data['first_name']
        if value=='': 
            raise forms.ValidationError("Please Enter Your name")
        return value

    def clean_last_name(self):
        value = self.cleaned_data['last_name']
        if value=='': 
            raise forms.ValidationError("Please Enter Your last name")
        return value
    
    def clean_email(self):
        value = self.cleaned_data['email']
        if value=='': 
            raise forms.ValidationError("email is not valid.")
        return value
    
    def clean_street_address(self):
        value = self.cleaned_data['street_address']
        if value=='': 
            raise forms.ValidationError("Please Enter Your Address")
        return value


    def clean_city_name(self):
        value = self.cleaned_data['city_name']
        if value=='': 
            raise forms.ValidationError("Please Enter Your City Name")
        return value
    
    def clean_state_name(self):
        value = self.cleaned_data['state_name']
        if value=='': 
            raise forms.ValidationError("Please Enter State Name")
        return value
    
    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        if value.isdigit()==False:
            raise forms.ValidationError("Only digit allows.")
        if value=='': 
            raise forms.ValidationError("Please Enter Your phone Number")
        
        if len(value) < 10:
            raise forms.ValidationError("Please Enter Your phone Number")
        return value
    
    
    def clean_zip_code(self):
        value = self.cleaned_data['zip_code']
        if value.isdigit()==False:
            raise forms.ValidationError("Only digit allows.")
        
        if value=='': 
            raise forms.ValidationError("Please Enter Your 6 Digit zip_code")
        
        if len(value) < 6:
            raise forms.ValidationError("Please Enter Your 6 Digit zip_code")
        return value




class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(render_value = True,attrs={"class": "form-control",'placeholder':'Enter old password'})
        self.fields["new_password1"].widget = forms.PasswordInput(render_value = True,attrs={"class": "form-control",'placeholder':'Enter new password'})
        self.fields["new_password2"].widget = forms.PasswordInput(render_value = True,attrs={"class": "form-control",'placeholder':'Enter confirm password'})
        