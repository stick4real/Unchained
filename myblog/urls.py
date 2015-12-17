from django.conf.urls import url

from . import views

app_name = 'myblog'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<article_id>[0-9]+)/$', views.article, name='article'),
    url(r'^article/new/$', views.newArticle, name='newArticle'),
    url(r'^article/delete/(?P<article_id>[0-9]+)$', views.deleteArticle, name='deleteArticle'),
    url(r'^article/(?P<article_id>[0-9]+)/comment/new/$', views.newComment, name='newComment'),
    url(r'^comment/delete/(?P<comment_id>[0-9]+)$', views.deleteComment, name='deleteComment'),
]