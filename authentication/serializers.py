from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import EmailField, CharField
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class RegisterSerializer(ModelSerializer):
    email = EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = CharField(required=True, validators=[validate_password], write_only=True)
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {
            'first_name': { 'required': True },
            'last_name': { 'required': True }
        }
    
    def create(self, validated_data):
        user = User.objects.create( 
            username= validated_data["username"],
            email= validated_data["email"],
            first_name= validated_data["first_name"],
            last_name= validated_data["last_name"]
        )

        user.set_password(validated_data["password"])
        user.save()
        return user
