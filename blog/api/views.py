from rest_framework.response import Response
from rest_framework import status  
from blog.models import Post,User,Sendrequest,Connection,Comment
from django.shortcuts import render,HttpResponseRedirect
from blog.api.serializers import Postapi,Registerview,Updateuser,Connectionapi,Sendrequestapi,Getrequestapi,Userapi,Postclass,Postlikeapi,Commentapi
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .pagination import Mypagination
from .custom import CustomAuthentication
from django.http import HttpResponse
from django.core.signing import TimestampSigner
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import generics
from rest_framework.views import APIView

class Postview(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = Postapi                                                                      
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=Mypagination


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            response = {
            "status": status.HTTP_201_CREATED,
            "message": "Data Created",
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author==request.user:
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status":status.HTTP_200_OK,
                    "message": "Data Updated",
                    }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_406_NOT_ACCEPTABLE,
                    "message": "You can not update this data",
                    }
                return Response(response,status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request, *args, **kwargs):
        try:
            if request.user:
                print('request.userrrrrrrrrr: ', request.user)
                queryset = Post.objects.filter(author=request.user)
                if not queryset:
                    response = {
                    "status":status.HTTP_404_NOT_FOUND,
                    "message": "user have no post",
                    }
                    return Response(response,status=status.HTTP_404_NOT_FOUND)
                serializer = Postapi(queryset, many=True)
                return Response(serializer.data)
            else:
                response = {
                    "status":status.HTTP_404_NOT_FOUND,
                    "message": "user not found",
                    }
                return Response(response,status=status.HTTP_404_NOT_FOUND)

        except:
                queryset=Post.objects.all()
                serializer=Postapi(queryset,many=True)
                return Response(serializer.data)
            
    def destroy(self, request, *args, **kwargs):
        try:
            post=Post.objects.filter(id=kwargs['pk']).first()
            print(post.author)
            if post:
                if post.author==request.user:
                    post.delete()
                    response = {
                            "status":status.HTTP_204_NO_CONTENT,
                            "message": "Data Deleted",
                                    }
                    return Response(response,status=status.HTTP_204_NO_CONTENT)
                else:
                    response = {
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "message": "You can not delete this Post",
                        }
                return Response(response,status.HTTP_401_UNAUTHORIZED)
            else:
                response = {
                    "status":status.HTTP_404_NOT_FOUND,
                    "message": "Post not found",
                    }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
        except:
                response = {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Data not found",}
                return Response(response,status=status.HTTP_404_NOT_FOUND)  

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print('instance: ', instance.like)
        serializer = self.get_serializer(instance)
        print('serializer: ', serializer)
        return Response(serializer.data)

        # response = {
        # "status": status.HTTP_404_NOT_FOUND,
        # "message": "Only sign up here",}
        # return Response(response,status=status.HTTP_404_NOT_FOUND)  
    

signer = TimestampSigner()

class Registerapi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class=Registerview
    pagination_class=Mypagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        token =signer.sign(user.id)
        subject ='This email is from django server'
        message= render_to_string('blog/link.html',
                {'user': user,
                'domain':'http://127.0.0.1:8000/verify/'+token,
                })
        from_email = settings.EMAIL_HOST_USER
        recipint_list= [user.email,]
        send_mail(subject=subject,message='hello',html_message=message,from_email=from_email,recipient_list=recipint_list,fail_silently=False)
        response = {
            "status":status.HTTP_201_CREATED,
            "message": "User Created",
            }
        return Response(response,status=status.HTTP_201_CREATED)

    # def list(self, request, *args, **kwargs):
    #     response = {
    #         "status":status.HTTP_201_CREATED,
    #         "message": "Only sign up here",
    #         }
    #     return Response(response,status=status.HTTP_201_CREATED)
    
    # def destroy(self, request, *args, **kwargs):
    #     response = {
    #     "status": status.HTTP_404_NOT_FOUND,
    #     "message": "Only sign up here",}
    #     return Response(response,status=status.HTTP_404_NOT_FOUND)  
        
    # def retrieve(self, request, *args, **kwargs):
    #     response = {
    #     "status": status.HTTP_404_NOT_FOUND,
    #     "message": "Only sign up here",}
    #     return Response(response,status=status.HTTP_404_NOT_FOUND)  

    # def update(self, request, *args, **kwargs):
        response = {
        "status": status.HTTP_404_NOT_FOUND,
        "message": "Only sign up here",}
        return Response(response,status=status.HTTP_404_NOT_FOUND)                  


class Manageuser(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=Registerview
    authentication_classes=[TokenAuthentication,SessionAuthentication]
    pagination_class=Mypagination

    def destroy(self, request, *args, **kwargs):
        try:
            user=User.objects.filter(id=kwargs['pk']).first()
            if user:
                if user.email==request.user:
                    user.delete()
                    response = {
                        "status":status.HTTP_204_NO_CONTENT,
                        "message": "Data Deleted",
                        }
                    return Response(response,status=status.HTTP_204_NO_CONTENT)
                else:
                    response = {
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "message": "You can not delete this User",}
                    return Response(response,status.HTTP_401_UNAUTHORIZED)
        except:
                response = {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Data not found",}
                return Response(response,status=status.HTTP_404_NOT_FOUND)  

    def update(self, request, *args, **kwargs):     
        instance = self.get_object()
        if instance==request.user:
            self.serializer_class=Updateuser
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    "status":status.HTTP_200_OK,
                    "message": "User Updated",
                    }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "Data not Updated",
                    }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

        else:
            response={
                "status":status.HTTP_406_NOT_ACCEPTABLE,
                "message": "You can not update this data of user",
                }
            return Response(response,status=status.HTTP_406_NOT_ACCEPTABLE)
                

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print('instanceeeeeeeeeeeeeeeeeeeee: ', instance)
        if instance==request.user:
            self.serializer_class=Updateuser
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        else:
            response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "Data not found",
                }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        #     queryset=User.objects.filter(email=request.user)
        #     serializer=Registerview(queryset,many=True)
        #     return Response(serializer.data)
                          

    def list(self, request, *args, **kwargs):
        try:
            if request.user:
                queryset = User.objects.filter(email=request.user)
                serializer = Registerview(queryset,many=True)
                return Response(serializer.data[0])
            else:
                response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "Data not found",
                }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
                # queryset=User.objects.filter(email=request.user)
                # serializer=Registerview(queryset,many=True)
                # return Response(serializer.data)
        except:
                
                response={
                    "status":status.HTTP_404_NOT_FOUND,
                    "message": "Data not found",
                    }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
            # queryset=User.objects.filter(email=request.user)
            # serializer=Registerview(queryset,many=True)
            # return Response(serializer.data)


class FollowersListView(generics.ListAPIView):
    queryset = Connection.objects.all()
    serializer_class = Connectionapi
    authentication_classes=[TokenAuthentication]

    def list(self, request, *args, **kwargs):
        # user=User.objects.filter(id=kwargs['pk']).first()
        if request.user:
                follower = Connection.objects.filter(follow_to=request.user).all()
                serializer = self.get_serializer(follower,many=True)
                if serializer:
                        response={
                                "status":'Follower list',
                                "data": serializer.data,
                                }  
                        return Response(response,status=status.HTTP_200_OK) 
        else:
                response={
                        "status":status.HTTP_204_NO_CONTENT,
                        "message": "No data",
                        }  
                return Response(response,status=status.HTTP_204_NO_CONTENT) 

class FollowingListView(generics.ListAPIView):
    queryset = Connection.objects.all()
    serializer_class = Connectionapi
    authentication_classes=[TokenAuthentication]

    def list(self, request, *args, **kwargs):
        try:
            if request.user:
                following = Connection.objects.filter(follow_by=request.user).all()
                serializer = self.get_serializer(following,many=True)
                if serializer:
                    response={
                            "status":'Following list',
                            "data": serializer.data,
                            }  
                    return Response(response,status=status.HTTP_200_OK)
                else:
                    response={
                    "status":status.HTTP_204_NO_CONTENT,
                    "data": 'following not exists',
                    }  
                    return Response(response,status=status.HTTP_204_NO_CONTENT)
            else:
                response={
                    "status":status.HTTP_204_NO_CONTENT,
                    "message": "No data",
                } 
                return Response(response,status=status.HTTP_204_NO_CONTENT)
        except:
                response={
                    "status":status.HTTP_404_NOT_FOUND,
                    "message": "Data not found",
                } 
                return Response(response,status=status.HTTP_404_NOT_FOUND)

        
class Unfollowview(generics.DestroyAPIView):
    queryset = Connection.objects.all()
    serializer_class = Connectionapi
    authentication_classes=[TokenAuthentication]

    def destroy(self, request, *args, **kwargs):
        user=User.objects.filter(id=kwargs['pk']).first()
        try:
            instance = Connection.objects.filter(follow_by=request.user,follow_to=user).first()
            # request_user=Sendrequest.objects.filter(requested_to=user).first()
            print('aaaaaaaaa',instance.follow_by)
            if instance.follow_by==request.user:
                instance.delete()
                # request_user.status='Rejected'
                # request_user.save()
                response={
                        "status":status.HTTP_301_MOVED_PERMANENTLY,
                        "message": "Unfollow user",
                        }
                return Response(response,status=status.HTTP_301_MOVED_PERMANENTLY)
            else:
                response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "This user Not in your follwing list",
                }  
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        except:
            response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "User Not found",
                }  
            return Response(response,status=status.HTTP_404_NOT_FOUND)
             


class Senderequestview(generics.CreateAPIView):
    queryset = Sendrequest.objects.all()
    serializer_class = Sendrequestapi
    authentication_classes=[TokenAuthentication,SessionAuthentication]

    def post(self, request, *args, **kwargs):
        user=User.objects.filter(id=kwargs['pk']).first()  
        if user==None:
                response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "User not found",
                }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
        print('user: ', user)
        serializer = Sendrequestapi(data={
                "requested_by":request.user.pk,
                "requested_to":user.pk,
        })
        print('serializerrrr: ', serializer)
        if serializer.is_valid(raise_exception=True):
            print('helooooooooooooooooo')
            serializer.save()
            response={
                "status":status.HTTP_201_CREATED,
                "message": "Your request sent",
                }
            return Response(response,status=status.HTTP_201_CREATED)
        else:
            response={
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "Data not valid",
                }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

                
class Getrequestview(generics.ListAPIView):
    queryset = Sendrequest.objects.all()
    serializer_class = Getrequestapi
    authentication_classes=[TokenAuthentication]
    
    def list(self, request, *args, **kwargs):
        queryset = Sendrequest.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        if serializer:
            return Response(serializer.data)
        else:
            response={
                "status":status.HTTP_204_NO_CONTENT,
                "message": "No data",
                }  
            return Response(response,status=status.HTTP_204_NO_CONTENT) 


class Connectionview(generics.CreateAPIView):
    queryset = Connection.objects.all()
    serializer_class = Connectionapi
    authentication_classes=[TokenAuthentication]

    def post(self, request, *args, **kwargs):
        user=Sendrequest.objects.filter(id=kwargs['pk']).first()
        if user!=None:
            print('user.requested_to==request.user: ', user.requested_to==request.user)
            if user.requested_to==request.user:
                serializer = Connectionapi(data={
                    "follow_by":user.requested_by.pk,
                    "follow_to":user.requested_to.pk,
                })
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    user.status='Accepted'
                    user.save()
                    response={
                            "status":status.HTTP_201_CREATED,
                            "message": "Your request Accepted",
                            }
                    return Response(response,status=status.HTTP_201_CREATED)
            else:
                response={
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "You can not accepte the request of this user",
                    }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     response={
            #         "status":status.HTTP_404_NOT_FOUND,
            #         "message": "User Not valid for accept the r",
            #     }
                # return Response(response,status=status.HTTP_404_NOT_FOUND)
        else:
                response={
                    "status":status.HTTP_404_NOT_FOUND,
                    "message": "Connection request not found",
                }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
             

class Rejectrequestview(generics.UpdateAPIView):
    queryset = Sendrequest.objects.all()
    serializer_class = Sendrequestapi
    authentication_classes=[TokenAuthentication]

    def update(self, request, *args, **kwargs):
        instance = Sendrequest.objects.filter(id=kwargs['pk']).first()
        if instance==None:
            response={
            "status":status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        if instance.status!='Rejected':           
            if instance.requested_to==request.user:
                instance.status='Rejected'
                instance.save()
                response={
                    "status":status.HTTP_301_MOVED_PERMANENTLY,
                    "message": "Request Rejected",
                    }
                return Response(response,status=status.HTTP_301_MOVED_PERMANENTLY)
            else:
                response={
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "You have no permission to Rejecte the request",
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)  
        else:
            response={
                    "status":status.HTTP_404_NOT_FOUND,
                    "message": "This user now not in your following list",
                }
            return Response(response,status=status.HTTP_404_NOT_FOUND)


class Cancelrequest(generics.DestroyAPIView):
    queryset = Sendrequest.objects.all()
    serializer_class = Sendrequestapi
    authentication_classes=[TokenAuthentication]

    def destroy(self, request, *args, **kwargs):
        instance = Sendrequest.objects.filter(id=kwargs['pk']).first()
        if instance==None:
            response={
            "status":status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        if instance.requested_by==request.user:
            instance.delete()
            response={
                "status":status.HTTP_200_OK,
                "message": "Request cancel",
                }
            return Response(response,status=status.HTTP_200_OK)
        else:
            response={
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "You can not cancel this request",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)  
         
        
class Requestlist(generics.ListAPIView):
    queryset = Sendrequest.objects.all()
    serializer_class = Sendrequestapi
    authentication_classes=[TokenAuthentication]

    def list(self, request, *args, **kwargs):
        try:
            if request.user:
                queryset=Sendrequest.objects.filter(requested_to=request.user,status='Pending').all()
                serializer = self.get_serializer(queryset,many=True)
                if serializer:
                    return Response(serializer.data[0])
                else:
                    response={
                    "status":status.HTTP_204_NO_CONTENT,
                    "message": "No data",
                    }  
                return Response(response,status=status.HTTP_204_NO_CONTENT)
            else:
                response={
                    "status":status.HTTP_404_NOT_FOUND,
                    "message": "User not found",
                    }  
                return Response(response,status=status.HTTP_404_NOT_FOUND)
        except:               
                response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "request list not found",
                }  
                return Response(response,status=status.HTTP_404_NOT_FOUND)


class Postlikeview(generics.CreateAPIView):
    queryset=Post.objects.all()
    serializer_class=Postlikeapi
    authentication_classes=[TokenAuthentication]

    def create(self, request, *args, **kwargs):
        if request.user:
            instance = Post.objects.filter(id=kwargs['pk']).first()
            user=User.objects.filter(email=request.user).first()
            if instance.like!=user:
                instance.like.add(user)
                instance.save()
                response={  
                    "status":status.HTTP_301_MOVED_PERMANENTLY,
                    "message": "You like the post",
                    }
                return Response(response,status=status.HTTP_301_MOVED_PERMANENTLY)
            else:
                response={
                "status":status.HTTP_409_CONFLICT,
                "message": "you already like this post",
                }  
                return Response(response,status=status.HTTP_409_CONFLICT) 
        else:
            response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "user not valid",
                }  
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        

class Postunlikeview(generics.DestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=Postlikeapi
    authentication_classes=[TokenAuthentication]
    
    def destroy(self, request, *args, **kwargs):
        instance = Post.objects.get(id=kwargs['pk'])
        # user=instance.get().like.filter(id=request.user.id)
        instance.like.remove(request.user)
        instance.unlike.add(request.user)
        instance.save()
        response={
                "status":status.HTTP_200_OK,
                "message": "you unlike the post",
                }  
        return Response(response,status=status.HTTP_200_OK)
        
class Commentview(generics.CreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=Commentapi
    authentication_classes=[TokenAuthentication]

    def create(self, request, *args, **kwargs):
        post=Post.objects.filter(id=kwargs['pk']).first()
        print('daaaaaaaaaaaaaaaaaaaa',request.data)
        if not request.data:
            response={
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "something went wrong",
                }  
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={
            'comment_by':request.user.pk,
            'post_name':post.pk,
            'comment':request.data['comment'],
        })
        if serializer.is_valid(raise_exception=True):   
            serializer.save()
            response={
                "status":status.HTTP_200_OK,
                "message": "comment sent successfully",
                }  
            return Response(response,status=status.HTTP_200_OK)
        
class Commentdelete(generics.DestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=Commentapi
    authentication_classes=[TokenAuthentication]

    def destroy(self, request, *args, **kwargs):
        instance=Comment.objects.filter(id=kwargs['pk']).first()
        # print('instanceeeeeeeeeeeee: ', instance)
        if instance==None:
            response={
            "status":status.HTTP_404_NOT_FOUND,
            "message": "Comment Not found",
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        if instance.comment_by==request.user:
            instance.delete()
            response={
                "status":status.HTTP_200_OK,
                "message": "comment Deleted sucssefullly",
                }
            return Response(response,status=status.HTTP_200_OK)
        else:
            response={
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "You can not delete this comment",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST) 
        
class Commentupdateview(generics.UpdateAPIView):
    queryset=Comment.objects.all()
    serializer_class=Commentapi
    authentication_classes=[TokenAuthentication]

    def update(self, request, *args, **kwargs):
            # comment=Comment.objects.filter(id=kwargs['pk']).first()
            comment = self.get_object()
            if comment==None:
                response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "Comment Not found",
                }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
            if request.user==comment.comment_by:
                serializer = self.get_serializer(comment,data=request.data)
                # print('serializerrrrrrrrrrrrrrrr: ', serializer)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    response={
                        "status":status.HTTP_200_OK,
                        "message": "comment update successfully",
                        }  
                    return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_200_OK,
                    "message": "You can not update this comment",
                    }  
                return Response(response,status=status.HTTP_200_OK)


class Commentlistview(generics.ListAPIView):
    queryset=Comment.objects.all()
    serializer_class=Commentapi
    authentication_classes=[TokenAuthentication]

    def list(self, request, *args, **kwargs):
        post=Post.objects.filter(id=kwargs['pk'])
        print('postttttttttttt: ', post.get())
        if not post:
            response={
            "status":status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            } 
            return Response(response,status=status.HTTP_404_NOT_FOUND)  
        queryset = Comment.objects.filter(post_name=post.get(),main_comment=None)
        print('querysetttttttttttt: ', queryset)
        serializer=self.get_serializer(queryset,many=True)
        # print('serializerrrrrrrrrrr: ', serializer)
        if serializer:
            return Response(serializer.data)



class Replyoncomment(generics.CreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=Commentapi
    authentication_classes=[TokenAuthentication]

    def create(self, request, *args, **kwargs):
        comment=Comment.objects.filter(id=kwargs['pk']).first()
        print('commenttttttttttttt: ', comment)
        if comment==None:
            response={
            "status":status.HTTP_404_NOT_FOUND,
            "message": "comment Not found",
            } 
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        if not request.data:
            response={
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "something went wrong",
                }  
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        # serializer = self.get_serializer(data=request.data,many=True)
        serializer = Comment.objects.create(comment_by=request.user,post_name=comment.post_name,comment=request.data['comment'],main_comment=comment)
        if serializer:
            serializer.save()
            response={
                "status":status.HTTP_200_OK,
                "message": "reply sent successfully",
                }  
            return Response(response,status=status.HTTP_200_OK)
        
class Getreplycomment(generics.ListAPIView):
    queryset=Comment.objects.all()
    serializer_class=Commentapi
    authentication_classes=[TokenAuthentication]


    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(id=kwargs['pk']).first()
        print('querysettttttttttttttt: ', queryset)
        if queryset==None:
            response={
            "status":status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            } 
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        try:
            reply=Comment.objects.filter(main_comment=queryset)
            serializer=self.get_serializer(reply,many=True)
            if serializer:
                return Response(serializer.data)
        except:
            response={
            "status":status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            }  
            return Response(response,status=status.HTTP_404_NOT_FOUND)
            
class Deletereplycomment(generics.DestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=Commentapi
    authentication_classes=[TokenAuthentication]


    def destroy(self, request, *args, **kwargs):
        serializer = Comment.objects.filter(id=kwargs['pk']).first()
        print('querysettttttttttttttt: ', serializer)
        if serializer==None:
            response={
            "status":status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            } 
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        try:
            if serializer.comment_by==request.user:
                serializer.delete()
                response={
                "status":status.HTTP_200_OK,
                "message": "Comment  deleted successfully",
                }  
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "you can not delete this comment",
                }  
                return Response(response,status=status.HTTP_404_NOT_FOUND)

        except:
            response={
            "status":status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            }  
            return Response(response,status=status.HTTP_404_NOT_FOUND)
            

class Updatereply(generics.UpdateAPIView):
    queryset=Comment.objects.all()
    serializer_class=Commentapi
    authentication_classes=[TokenAuthentication]

    def update(self, request, *args, **kwargs):
            comment=Comment.objects.filter(id=kwargs['pk']).first()
            # comment = self.get_object()
            if comment==None:
                response={
                "status":status.HTTP_404_NOT_FOUND,
                "message": "Comment Not found",
                }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
            if request.user==comment.comment_by:
                serializer = self.get_serializer(comment,data={'comment':request.data['comment']})
                # print('serializerrrrrrrrrrrrrrrr: ', serializer)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    response={
                        "status":status.HTTP_200_OK,
                        "message": "reply update successfully",
                        }  
                    return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_200_OK,
                    "message": "You can not update this comment",
                    }  
                return Response(response,status=status.HTTP_200_OK)
