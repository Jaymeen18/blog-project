from django import forms
from blog.models import Post,User,Sendrequest,Sendrequest,Connection,Comment
from blog.forms import Signupform
from rest_framework import serializers

from django.contrib.auth.hashers import make_password

class Likedby(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email']

class Commentby(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','comment','comment_by']

class Postapi(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    total_like=serializers.SerializerMethodField(read_only=True)
    total_unlike=serializers.SerializerMethodField(read_only=True)
    total_comments=serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = Post 
        fields = ['id','title','desc','author','created_at','total_like','total_unlike','total_comments']

    def get_total_comments(self,obj):
        print('objjjjjjjjjjjj: ', obj.author)
        return Comment.objects.filter(post_name=obj).count()

    def get_total_like(self, obj):
        # obj.liked_by.count()
        return obj.like.count()
    
    def get_total_unlike(self, obj): 
        # obj.liked_by.count()
        return obj.unlike.count()
    
    def validate_title(self,value):
        if value=='':
            raise serializers.ValidationError("Please Enter a title.")      
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
    
    def validate_desc(self,value):
        print('aaaaaaaagaaaaaaaabbbbb',value)
        if value=='':
            raise serializers.ValidationError("Please Enter a Descriptions.")      
        if len(value) < 20:
            raise serializers.ValidationError("Descriptions Must be 20 characters long.")
        return value

   
class Postclass(serializers.ModelSerializer):
    total_like=serializers.SerializerMethodField(read_only=True)
    total_unlike=serializers.SerializerMethodField(read_only=True)
    total_comments=serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = Post 
        fields = fields = ['id','title','desc','author','created_at','total_like','total_unlike','total_comments']

    def get_total_like(self, obj):
        # obj.liked_by.count()
        return obj.like.count()
    
    def get_total_unlike(self, obj):
        # obj.liked_by.count()
        return obj.unlike.count()
    
    def get_total_comments(self,obj):
        print('objjjjjjjjjjjj: ', obj.author)
        return Comment.objects.filter(post_name=obj).count()


class Followercount(serializers.ModelSerializer):
    # followers_count = serializers.IntegerField(read_only=True)
    class Meta:
        model=Connection
        fields='__all__'

    
class Registerview(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True,required=True,
    style={'input_type': 'password'})

    password2 = serializers.CharField(write_only=True,required=True,
    style={'input_type': 'password'})
    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)
    post=Postclass(many=True,source='author',read_only=True) 
    total_post = serializers.SerializerMethodField(read_only=True)

       
    class Meta:
        model = User
        fields=['id','email','first_name','last_name','date_of_birth','street_address','city_name','state_name','zip_code','phone_number','password','password2','gender','bio','link','followers','following','total_post','post'] 

    def get_followers(self, obj):
        return Connection.objects.filter(follow_to=obj).count()
    
    def get_following(self, obj):
        return Connection.objects.filter(follow_by=obj).count()
    
    def get_total_post(self, obj):
        # Calculate the total number of posts associated with the user
        return obj.author.count()
    
    def validate_email(self, value):    
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    def validate_first_name(self, value):    
        if value=='':
            raise serializers.ValidationError("Please Enter Your Name.")
        return value
    
    def validate_last_name(self, value):    
        if value=='':
            raise serializers.ValidationError("Please Enter Your Last Name.")
        return value

    
    def validate_street_address(self, value):
        if value=='':
            raise serializers.ValidationError("Please Enter Your Address.")
        return value

    def validate_city_name(self, value):
        if value=='':
            raise serializers.ValidationError("Please Enter Your City Name.")
        return value
    
    def validate_state_name(self, value):
        if value=='':
            raise serializers.ValidationError("Please Enter Your State Name.")
        return value

    def validate_phone_number(self,value):
        if value.isdigit()==False:
            raise serializers.ValidationError("only digit allows.")
        if value==None:
            raise serializers.ValidationError("Entet a moboile number")
                  
        if len(value) < 10:
            raise serializers.ValidationError("This mobile Number is not valid")
        
        return value

    def validate_zip_code(self,value):
        if value.isdigit()==False:
            raise serializers.ValidationError("only digit allows.")
        if value==None:
            raise serializers.ValidationError('This field is requried')
        if len(value) < 6:
            raise serializers.ValidationError("This Zip code is not valid")
        return value

    def validate_password(self, value):
        data = self.get_initial()
        password = data.get('password2')
        password2 = value
        if password != password2:
            raise serializers.ValidationError('Passwords must match')
        return value
    
    def create(self, validated_data):
        if validated_data.get('password') != validated_data.get('password2'):
            raise serializers.ValidationError("Those password don't match") 
        elif validated_data.get('password') == validated_data.get('password2'):
            validated_data['password'] = make_password(validated_data.get('password'))
            validated_data.pop('password2')
        return super(Registerview,self).create(validated_data)
    
class Updateuser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','email','first_name','last_name','date_of_birth','street_address','city_name','state_name','zip_code','phone_number','gender','bio','link'] 


    def validate_phone_number(self,value):
        if len(value) < 10:
            raise serializers.ValidationError("This mobile Number is not valid")
        return value

    def validate_zip_code(self,value):
        if value==None:
            raise serializers.ValidationError('This field is requried')
        if len(value) < 6:
            raise serializers.ValidationError("This Zip code is not valid")
        return value

    def validate_first_name(self, value):    
        if value=='':
            raise serializers.ValidationError("Please Enter Your Name.")
        return value

    def validate_last_name(self, value):    
        if value=='':
            raise serializers.ValidationError("Please Enter Your Last Name.")
        return value

    def validate_street_address(self, value):
        if value=='':
            raise serializers.ValidationError("Please Enter Your Address.")
        return value

    def validate_city_name(self, value):
        if value=='':
            raise serializers.ValidationError("Please Enter Your City Name.")
        return value
    
    def validate_state_name(self, value):
        if value=='':
            raise serializers.ValidationError("Please Enter Your State Name.")
        return value

class Userapi(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','first_name','last_name','city_name']


class Sendrequestapi(serializers.ModelSerializer):
    requested_by=Userapi(read_only=True)
    requested_to=Userapi(read_only=True)
    class Meta:
        model=Sendrequest
        fields = ['requested_by','requested_to','status']


    def validate(self, data):
        requested_by = data.get('requested_by')
        requested_to = data.get('requested_to')                                       
        existing_request = Sendrequest.objects.filter(requested_by=requested_by, requested_to=requested_to).exists()
        if existing_request:
            raise serializers.ValidationError("You already sent a request to this user")
        
        if data['requested_by']==data['requested_to']:
            raise serializers.ValidationError("You can not sent Request to your self")
        return data        

    def validate_requested_by(self,value):
        if value==None:
            raise serializers.ValidationError("User not found")
        return value
    
    def validate_requested_to(self,value):
        if value==None:
            raise serializers.ValidationError("User not found")
        return value
    
class Getrequestapi(serializers.ModelSerializer):
    class Meta:
        model=Sendrequest
        fields = ['requested_by','requested_to','status','created_at']
        # fields='__all__'


class Connectionapi(serializers.ModelSerializer):
    class Meta:
        model=Connection
        fields = ['follow_by','follow_to','created_at']

    def validate(self, data):
        follow_by = data.get('follow_by')
        follow_to = data.get('follow_to')

        existing_request = Connection.objects.filter(follow_by=follow_by, follow_to=follow_to).exists()
        if existing_request:
            raise serializers.ValidationError("This user is already in your followers list")
        return data
    

class Postlikeapi(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['liked_by']


class Userapi1(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','first_name','last_name','city_name']

        
class Commentapi(serializers.ModelSerializer):
    comment_by=Userapi1(read_only=True)
    class Meta:
        model=Comment
        fields='__all__'

    def validate_comment_by(self,value):
        if value==None:
            raise serializers.ValidationError("This field is required")
        return value
    
    def validate_comment(self,value):
        if value=='':
            raise serializers.ValidationError("This field is required")
        return value