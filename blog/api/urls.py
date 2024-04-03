from django.urls import path,include
from blog.api import views
from rest_framework.routers import DefaultRouter

router  = DefaultRouter()

router.register('crud',views.Postview,basename='post')
# router.register('crud/<int:pk>/',views.UpdateIsFav,basename='postisFav')
# router.register('signup',views.Registerapi,basename='signup')
router.register('manage',views.Manageuser,basename='Manage')
# router.register('getrequest',views.Getrequestview,basename='getrequest')

urlpatterns = [
    path('followers-list/', views.FollowersListView.as_view(), name='followers-list'),
    path('signup/', views.Registerapi.as_view(), name='signup'),
    path('following-list/', views.FollowingListView.as_view(), name='following-list'),
    path('send-request/<int:pk>/', views.Senderequestview.as_view(), name='send-request'),
    path('list-request/', views.Getrequestview.as_view(), name='list-request'),
    path('accept-request/<int:pk>/', views.Connectionview.as_view(), name='accept-request'),
    path('delete-request/<int:pk>/', views.Rejectrequestview.as_view(), name='delete-request'),
    path('unfollow-user/<int:pk>/', views.Unfollowview.as_view(), name='unfollow-user'),
    path('cancel-request/<int:pk>/', views.Cancelrequest.as_view(), name='accept-request'),
    path('request-list/', views.Requestlist.as_view(), name='request-list'),
    path('post-like/<int:pk>/', views.Postlikeview.as_view(), name='post-like'),
    path('post-unlike/<int:pk>/', views.Postunlikeview.as_view(), name='post-unlike'),
    path('comment/<int:pk>/', views.Commentview.as_view(), name='comment'),
    path('comment-delete/<int:pk>/', views.Commentdelete.as_view(), name='comment-delete'),
    path('comment-update/<int:pk>/', views.Commentupdateview.as_view(), name='comment-update'),
    path('comment-update/<int:pk>/', views.Commentupdateview.as_view(), name='comment-update'),
    path('comment-list/<int:pk>/', views.Commentlistview.as_view(), name='comment-list'),
    path('reply/<int:pk>/', views.Replyoncomment.as_view(), name='comment-reply'),
    path('list-reply/<int:pk>/', views.Getreplycomment.as_view(), name='list-reply'),
    path('delete-reply/<int:pk>/', views.Deletereplycomment.as_view(), name='delete-reply'),
    path('update-reply/<int:pk>/', views.Updatereply.as_view(), name='update-reply'),
    path('list_user/', views.Userlist.as_view(), name='user_list'),
    path('crud/<int:pk>/',views.UpdateIsFavAsTrue.as_view(),name='postisFav'),
    path('remove/Isfav/<int:pk>/',views.UpdateIsFavasFlase.as_view(),name='postnotisFav'),
    path('',include(router.urls))
]