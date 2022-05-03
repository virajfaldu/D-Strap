from django.urls import path
from . import views
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('categories/<str:name>',views.categories,name="category"),
    path('blog',views.blog,name="blog"),
    path('about',views.about,name="about"),
    path('post_details/<str:title>',views.post_detail,name="post_details"),
    path('add_post',views.add_post,name="add_post"),
    path('like/<str:title>',views.likes,name="like"),
    path('comment/<str:title>',views.add_comment,name="comment"),
    path('search',views.search,name="search"),

     
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
