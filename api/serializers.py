from rest_framework import serializers
from vacation.models import Vacation, Country, Like
from django.contrib.auth import get_user_model
from datetime import date

user=get_user_model()

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