from rest_framework import serializers
from vacation.models import Vacation, Country, Like
from django.contrib.auth import get_user_model,authenticate
from datetime import date
from django.contrib.auth.password_validation import validate_password

User=get_user_model()

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'vacation']

class VacationSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), source='country', write_only=True)   
    liked_by = serializers.SlugRelatedField(many=True, read_only=True,slug_field='username')
    image = serializers.ImageField(required=False)
    class Meta:
        model = Vacation
        fields = ['id', 'country','country_id', 'description', 'start_date', 'end_date', 'image', 'price', 'liked_by']

    def validate(self, data):
        request = self.context.get('request')
        is_update = request and request.method in ['PUT', 'PATCH']
        start_date=data.get('start_date')
        end_date=data.get('end_date')
        today = date.today()
        if not is_update:
            if start_date and start_date < today:
                raise serializers.ValidationError({"start_date": "Start date must be in the future."})
            if end_date and end_date < today:
                raise serializers.ValidationError({"end_date": "End date should not be in the past."})
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"end_date": "End date must be after start date."})
        
        return data
    
class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password', 'password2', 'role']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user=User.objects.create_user(**validated_data)
        return user
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user=serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        user=authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Email or password is incorrect.")
        if not user.is_active:
            raise serializers.ValidationError("User is disabled.")
        
        data['user'] = user
        return data
        
    



