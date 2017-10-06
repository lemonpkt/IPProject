from rest_framework import serializer
from .models import Project,Review

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model=Project
        fields='__all__'
        
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model=Review
        fields='__all__'
        
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserProfile
        fields='__all__'