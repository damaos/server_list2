from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    url(r'^list/', views.ServerList.as_view(), name='list'),
    url(r'^server/new', views.ServerNewView.as_view(), name="newserver"),
    url(r'^assign/new', views.NewAssignView.as_view(), name="newassign"),
    url(r'^assignClient/new', views.NewAssignClientView.as_view(), name="newassignclient"),
    url(r'^client/new', views.NewClientView.as_view(), name="newclient"),
    url(r'^interface/new', views.NewInterfaceView.as_view(), name="newinterface"),
    url(r'^platform/new', views.NewPlatformView.as_view(), name="newplatform"),
    url(r'^server/edit/(?P<id>\d+)/$', views.ServerEditView.as_view(), name='editserver'),
    url(r'^assign/edit/(?P<id>\d+)/$', views.AssignEditView.as_view(), name='editassign'),
    url(r'^assignClient/edit/(?P<id>\d+)/$', views.AssignClientEditView.as_view(), name='editassignclient'),
    url(r'^client/edit/(?P<id>\d+)/$', views.ClientEditView.as_view(), name='editclient'),
    url(r'^interface/edit/(?P<id>\d+)/$', views.InterfaceEditView.as_view(), name='editinterface'),
    url(r'^platform/edit/(?P<id>\d+)/$', views.PlatformEditView.as_view(), name='editplatform'),
    url(r'^server/detail/(?P<id>\d+)/$', views.ServerDetailView.as_view(), name='detailserver'),
   
   

]