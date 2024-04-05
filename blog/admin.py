from django.contrib import admin
from .models import Post,User,Sendrequest,Connection,Comment

# Register your models here.

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display=['id','title','desc','author','created_at','liked_by','unliked_by','isFavorite']
    
@admin.register(User)
class Useradmin(admin.ModelAdmin):
    list_display = ['id','email','first_name','last_name','date_of_birth','street_address','city_name','state_name','zip_code','phone_number','gender','bio','link']


@admin.register(Sendrequest)
class Profileadmin(admin.ModelAdmin):
    list_display=['id','requested_by','requested_to','status','created_at']


@admin.register(Connection)
class Profileadmin(admin.ModelAdmin):
    list_display=['id','follow_by','follow_to','created_at']

@admin.register(Comment)
class Commentadmin(admin.ModelAdmin):
    list_display=['id','comment_by','post_name','comment','main_comment']
