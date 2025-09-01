from rest_framework import serializers
from account.models import User

class UserRegistrationsSerializer(serializers.Serializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
        )    
    class Meta:
        model = User 
        fields ='__all__'
        extra_kwargs = {
            'password':{'write_only':True}
        }
        