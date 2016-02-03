from django.conf.urls import include, url
from django.contrib import admin

from qpanda import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name='index'),

    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),

    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),

    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    url(r'^askquestion/$', views.askquestion, name='askquestion'),

    url(r'^question/$', views.question, name='question'),

]