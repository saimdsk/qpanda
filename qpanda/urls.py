from django.conf.urls import include, url
from django.contrib import admin

from qpanda import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.askquestion, name='askquestion'),
    # changed this to point straight to the askquestion page. We don't need to load a page, click a button, load another
    # page before we actually do what we want to do.

    url(r'^askquestion/$', views.askquestion, name='askquestion'),

    url(r'^question/$', views.question, name='question'),

]
