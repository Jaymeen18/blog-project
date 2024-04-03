from typing import Any, Optional
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin
from .mangers import UserManager
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# Create your models here.



# class CustomUserMangaer(UserManager):
#     def _create_user(self,email,password,**extra_fields):
#         if not email:
#             raise ValueError('Email is not valid')
        
#         email = self.normalize_email
#         user = self.model(email=email,**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user
    
#     def create_user(self, email=None , password=None, **extra_fields):
#         extra_fields.setdefault('is_staff',False)
#         extra_fields.setdefault('is_superuser',False)
#         return self._create_user(email,password,**extra_fields)
    
#     def create_superuser(self,email=None , password=None, **extra_fields: Any):
#         extra_fields.setdefault('is_staff',True)
#         extra_fields.setdefault('is_superuser',True)
#         return self._create_user(email,password,**extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):
    first  = 'Male'
    second = 'Female'

    status_list = [(first,'Male'),(second,'Female')]

    email = models.EmailField(blank=True,default='',unique=True)
    first_name=models.CharField(max_length=20,blank=True,default='')
    last_name=models.CharField(max_length=20,blank=True,default='')
    date_of_birth=models.DateField(null=True)
    street_address=models.CharField(max_length=200,blank=True,default='')
    city_name=models.CharField(max_length=20,blank=True,default='')
    state_name=models.CharField(max_length=20,blank=True,default='')
    zip_code=models.CharField(max_length=6,null=True)
    phone_number=models.CharField(max_length=12,null=True)
    gender = models.CharField(max_length=10,choices=status_list)
    bio = models.TextField(max_length=100,blank=True,default='')
    link = models.CharField(max_length=100,blank=True,default='')



    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified=models.BooleanField(default=False)
    is_blocked_by_admin=models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True,null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS=[]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.first_name +' '+self.last_name
    def get_short_name(self):
        return self.email.split('@')[0]
    

class Post(models.Model):
    title=models.CharField(max_length=150)
    desc=models.TextField() 
    author= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='author')
    like=models.ManyToManyField(User,related_name='liked_by')
    unlike=models.ManyToManyField(User)
    created_at=models.DateTimeField(default=timezone.now)
    isFavorite=models.BooleanField(default=False)


    def liked_by(self):
        return ",".join([str(p) for p in self.like.all()])
    
    def unliked_by(self):
        return ",".join([str(p) for p in self.unlike.all()])

#This signal  creates Auth token for Users
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance) 


class Sendrequest(models.Model):
    pending  = 'Pending'
    accepted = 'Accepted'
    rejected = 'Rejected'
    status_list = [(pending,'Pending'),(accepted,'Accepted'),(rejected,'Rejected')]

    requested_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='requested_by')
    requested_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='requested_to')
    status = models.CharField(max_length=10,choices=status_list,default='Pending')
    created_at=models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        if self.requested_by is None:
            self.user_settings = User.get_default_params()
        super(Sendrequest, self).save(*args, **kwargs)

class Connection(models.Model):
    follow_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='follow_by')
    follow_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='follow_to')
    created_at=models.DateTimeField(default=timezone.now)


class Comment(models.Model):    
    comment_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='comment')
    post_name=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True,related_name='post_name')
    comment=models.CharField(max_length=200,null=True,blank=True)
    main_comment=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,related_name="replies", null=True)
