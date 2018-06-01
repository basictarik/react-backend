from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^', include('crud_project.urls')),
    path('admin/', admin.site.urls),
]
