from django.conf.urls import url, include

from .views import *

urlpatterns =[
    url(r'^estudiantes/$', estudiantes),
    url(r'^estudiantes/(?P<pk>\w+)/$', estudianteDetail),
    url(r'^psicologos/$', psicologos),
    url(r'^psicologos/(?P<pk>\w+)/$', psicologoDetail),
    url(r'^horarios/$', horarios),
    url(r'^horarios/(?P<pk>\w+)/$', horarioDetail),
    url(r'^citas/$', citas),
    url(r'^citas/(?P<pk>\w+)/$', citaDetail),
]