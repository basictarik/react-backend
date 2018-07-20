from django.conf.urls import url
from crud_project import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^posts/$', views.post_list),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'signup/$', views.register_user),
    url(r'^profiles/(?P<username>[%&+ \w]+)/$', views.update_user_profile),
    url(r'^login/', obtain_jwt_token),
    url(r'^token_renew/', refresh_jwt_token),
]