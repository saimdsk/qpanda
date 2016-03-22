from django.conf.urls import include, url
from django.contrib import admin

from qpanda import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.ask_question, name='ask_question'),
    # changed this to point straight to the ask_question page. We don't need to load a page, click a button, load
    # another page before we actually do what we want to do.

    url(r'^ask_question/$', views.ask_question, name='ask_question'),

    url(r'^question/$', views.question, name='question'),

]
