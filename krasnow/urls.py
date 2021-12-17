from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('csv2db.urls')),
    # url(r'^neuronid/', include('neuronid.urls', namespace="neuronid")),
    # url(r'^admin/', include(admin.site.urls)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
