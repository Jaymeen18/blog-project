from django.shortcuts import redirect, render,HttpResponseRedirect,HttpResponse
from django.urls import reverse, reverse_lazy
from .forms import Signupform,loginform,Postform,Updateprofile,PasswordChangeForm
from django.contrib import messages
from .models import Post
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from .models import User
from django.template.loader import render_to_string
from django.core.signing import TimestampSigner
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash




signer = TimestampSigner()
# token = signer.sign(user_id)  # Replace user_id with the user's ID
# from rest_framework import status

# Create your views here.
def homeview(request):
    posts = Post.objects.all() 
    paginator = Paginator(posts,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'blog/home.html',{'posts':page_obj})

def aboutview(request):
    return render(request,'blog/about.html')

def contactview(request):
    return render(request,'blog/contact.html')

#Dashboard
def dashboardview(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'user':request.user})
    else:
       return HttpResponseRedirect('/login/')


#Regster
def signupview(request):
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():
            messages.success(request,'Please confirm your email address to complete the registration')
            user = form.save()
            # form = Signupform()
            token =signer.sign(user.id)
            subject ='This email is from django server'
            message= render_to_string('blog/link.html',
                {'user': user,
                'domain':'http://127.0.0.1:8000/verify/'+token,
                })
            from_email = settings.EMAIL_HOST_USER
            recipint_list= [user.email,]
            send_mail(subject=subject,message='hello',html_message=message,from_email=from_email,recipient_list=recipint_list,fail_silently=False)
            form = Signupform()
        return render(request,'blog/signup.html',{'form':form})
            # return HttpResponseRedirect('/signup/')     
        # else:
        #     return HttpResponseRedirect('/signup/')
    else:
        if not request.user.is_authenticated:
            form = Signupform()
            return render(request,'blog/signup.html',{'form':form})
        else:
            return HttpResponseRedirect('/dashboard/')
#Login

def verify(request,token):
    user_id = signer.unsign(token)
    user= User.objects.get(id=user_id)
    user.is_email_verified=True
    user.save()
    return HttpResponseRedirect('/login/')

      


def loginview(request):
    if not request.user.is_authenticated:
        if request.method =='POST':
            form_object = loginform(request=request,data=request.POST)
            if form_object.is_valid():
                username=form_object.cleaned_data['username']
                password=form_object.cleaned_data['password']
                check_valid=authenticate(username=username,password=password)
                if check_valid is not None:
                    user = User.objects.get(email=check_valid)
                    if user.is_email_verified==True:
                        if user.is_blocked_by_admin==False:
                            login(request,check_valid)
                            messages.success(request,"Logged in Successfully !!")
                            return HttpResponseRedirect('/dashboard/')
                    else:
                        messages.success(request,'Your email is not verified,Please first verify your email.')
                        # return HttpResponseRedirect('/login/')
                    # messages.success(request,"Logged in Successfully !!")
                    return HttpResponseRedirect('/dashboard/')
                else:
                    messages.success(request,'llllllllllllll.')
                    # return redirect('login')
            else:
                messages.success(request,'You have entered wrong email or password')
                # return HttpResponseRedirect('/login/')
        else:
            form_object = loginform()
        return render(request,'blog/login.html',{'form_object':form_object})
    else:
        return HttpResponseRedirect('/dashboard/')


# Logout
def logoutview(request):
    logout(request)
    return HttpResponseRedirect('/')

#Add new post

def addpost(request):
   if request.user.is_authenticated:
        if request.method == 'POST': 
            formobject=Postform(request.POST)
            if formobject.is_valid():
                title = formobject.cleaned_data['title']
                desc = formobject.cleaned_data['desc']
                postdata=Post(title=title,desc=desc,author=request.user)
                postdata.save()
                messages.success(request,'You are add new post successfully!!!')
                formobject=Postform()
                return HttpResponseRedirect('/dashboard/')
        else:
            formobject=Postform()
        return render(request,'blog/addpost.html',{'form':formobject})
   else:
      return HttpResponseRedirect('/login/')
   
#update post

def updatepost(request,id):
   if request.user.is_authenticated:
        if request.method == 'POST': 
                getdata=Post.objects.get(id=id)
                formobject=Postform(request.POST,instance=getdata)
                if formobject.is_valid():
                    formobject.save()
                    messages.success(request,'You updated post successfully!!!')
                    formobject=Postform()
                    return HttpResponseRedirect('/dashboard/')
                return render(request,'blog/updatepost.html',{'form':formobject})
                    # return HttpResponseRedirect('/login/')
                # else:
                #     messages.error(request,'Please Enter a valid data')
                #     return HttpResponseRedirect(reverse('updatepost', kwargs={'id':id}))
        else:
                get_data = Post.objects.get(id=id)
                if request.user==get_data.author:
                    formobject=Postform(instance=get_data)
                    return render(request,'blog/updatepost.html',{'form':formobject})
                else:
                    return HttpResponseRedirect('/dashboard/')
   else:
      return HttpResponseRedirect('/login/')
   

#deletepost
def deletepost(request,id):
    if request.method == 'POST':
        delete_post = Post.objects.get(id=id)
        delete_post.delete()    
        return HttpResponseRedirect('/dashboard/')


def profielview(request):
    if request.user.is_authenticated:
        user=request.user
        user_profile = User.objects.get(email=user)
        post = Post.objects.all()
        return render(request,'blog/profile.html',{'user':user_profile,'posts':post})
    
def updateprofile(request,id):
    if request.method == 'POST':
        update_user = User.objects.get(id=id)
        form = Updateprofile(request.POST,instance=update_user)
        if form.is_valid():
            form.save()
            messages.success(request,'Your profile is updated.')
            return HttpResponseRedirect('/profile/')
        user_profile = User.objects.get(id=id)
        return render(request,'blog/updateprofile.html',{'user':user_profile,'form':form})     
    else:
        if  request.user.is_authenticated:
            update_user = User.objects.get(id=id)
            form = Updateprofile(instance=update_user)     
            return render(request,'blog/updateprofile.html',{'form':form})
        else:
            return HttpResponseRedirect('/login/')




def addpost2(request):
   if request.user.is_authenticated:
      if request.method == 'POST': 
        formobject=Postform(request.POST)
        if formobject.is_valid():
            title = formobject.cleaned_data['title']
            desc = formobject.cleaned_data['desc']
            postdata=Post.objects.create(title=title,desc=desc,author=request.user)
            postdata.save() 
            messages.success(request,'You are add new post successfully!!!')
            return HttpResponseRedirect('/profile/')
        return render(request,'blog/addpost2.html',{'form':formobject,'user':request.user})
      else:
        formobject=Postform()
        user=request.user
      return render(request,'blog/addpost2.html',{'form':formobject,'user':user})
   else:
      return HttpResponseRedirect('/login/')
   

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changepass')
        # else:
        #     messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'blog/changepass.html', {
        'form': form
    })