from rest_framework import serializers
from filer.models import Folder, Image
from .models import Video


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields= ('id', 'name', 'created_at', 'uploaded_at', 'modified_at', 
                'level','parent')
        extra_kwargs = {'parent': {'write_only': True}}
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields= ('id', 'name', 'folder', 'owner','file', 'uploaded_at', 'modified_at')
        
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields= ('id', 'name', 'folder','owner','file', 'uploaded_at', 'modified_at')