from rest_framework import serializers
from app.models import *
class UserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact  # Make sure this line is present
        fields = '__all__'
        
class FCM_tokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCM_token  # Make sure this line is present
        fields = '__all__'
        