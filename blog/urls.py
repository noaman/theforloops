from django.urls import path
from django.conf.urls import include, url
from . import views
app_name = 'blog'
urlpatterns=[
    path('',views.index,name="index"),
    #path('tag/<slug:tag_slug>/',views.post_list, name='post_tag'), 
    # path('<slug:post>/',views.post_detail,name="post_detail"),
    # path('<slug:post>/',views.post_detail,name="post_detail"),

    url(r'^post/(?P<id>.*)/(?P<slug>.*)/$', views.post_detail,name='post_detail'),

    
    path('about',views.about,name="about"),
    url(r'^category/(?P<category>.*)/(?P<category_id>.*)/$', views.category_list,name='category_list'),
    url(r'^category/(?P<category>.*)/$', views.category_list,name='category_list'),
    url(r'^tag/(?P<tag>.*)/$', views.tag_list,name='tag_list'),

    url(r'^updateclaps/(?P<pid>.*)/$', views.update_claps,name='update_claps'),
]   