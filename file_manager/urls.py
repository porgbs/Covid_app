from django.conf.urls import url
from .views import ( FolderView, SubFolderView, FolderDetailView,
                    ImageByFolderView, ImageView, ImageDetailView,
                    VideoDetailView, VideoByFolderView, VideoView)

urlpatterns = [
    url(r'^folder/$', FolderView.as_view(), name='file_manager_folder'),
    url(r'^folder/(?P<pk>\d+)/$', FolderDetailView.as_view(), name='file_manager_folder_detail'),
    url(r'^folder/(?P<pk>\w+)/sub/$', SubFolderView.as_view(), name='file_manager_sub_folder'),
    url(r'^folder/(?P<pk>\w+)/image/$', ImageByFolderView.as_view(), name='file_manager_folder_image'),
    url(r'^image/$', ImageView.as_view(), name='file_manager_image'),
    url(r'^image/(?P<pk>\d+)/$', ImageDetailView.as_view(), name='file_manager_image_detail'),
    url(r'^video/$', VideoView.as_view(), name='file_manager_video'),
    url(r'^folder/(?P<pk>\w+)/video/$', VideoByFolderView.as_view(), name='file_manager_folder_video'),
    url(r'^video/(?P<pk>\d+)/$', VideoDetailView.as_view(), name='file_manager_video_detail'),
]