from django.conf.urls import url
from . import views

app_name = 'myblog'
urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name = 'index'),
        url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name = 'detail'),
        url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name = 'archives'),
        url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name = 'category'),
        url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name = 'tag'),
        #url(r'^post/publish$', views.post_publish, name = 'post_publish'),
        #url(r'^post/edit/(?P<pk>[0-9]+)$', views.post_edit, name = 'post_edit'),
        url(r'^post/publish$', views.PostPublishView.as_view(), name = 'post_publish'),
        url(r'^post/edit/(?P<pk>[0-9]+)$', views.PostEditView.as_view(), name = 'post_edit'),
        ]
