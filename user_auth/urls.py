from django.conf.urls import include, url
from .views import SignupView, IsUserExist, IsActiveUser, UpdateUserRole

urlpatterns = [
    url(r'', include('rest_auth.urls')),
    url(r'^signup/$', SignupView.as_view(), name='user_auth_rest_register'),
    url(r'^user-exist/$', IsUserExist.as_view(), name='user_exist'),
    url(r'^user-status/(?P<pk>\d+)/$', IsActiveUser.as_view(), name='user_status'),
    url(r'^user-role/(?P<pk>\d+)/$', UpdateUserRole.as_view(), name='user_role'),
]