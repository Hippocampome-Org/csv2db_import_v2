from django.conf.urls import url
from csv2db import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^import_all/$', views.import_all, name='import_all'),
    # url(r'^import_article/$', views.import_article, name='import_article'),
    # url(r'^import_attachment/$', views.import_attachment, name='import_attachment'),
    # url(r'^import_connection/$', views.import_connection, name='import_connection'),
    # url(r'^import_epdata/$', views.import_epdata, name='import_epdata'),
    # url(r'^import_fragment/$', views.import_fragment, name='import_fragment'),
    # url(r'^import_markerdata/$', views.import_markerdata, name='import_markerdata'),
    # url(r'^import_morphdata/$', views.import_morphdata, name='import_morphdata'),
    # url(r'^import_notes/$', views.import_notes, name='import_notes'),
    # url(r'^import_synonym/$', views.import_synonym, name='import_synonym'),
    # url(r'^import_term/$', views.import_term, name='import_term'),
    # url(r'^import_type/$', views.import_type, name='import_type'),
    # url(r'^import_type_dev/$', views.import_type_dev, name='import_type_dev'),
    url(r'^load/$', views.load, name='load'),
]
