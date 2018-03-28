from django.conf.urls import url
from . import views
urlpatterns = [
    url('^register/', views.RegisterView),
    url('^nextqn/', views.NextQnView),
    url('^correctans/', views.CorrectAnsView),
    url('^finally/', views.FinallyView),
    url('^leader/', views.LeaderView)
]