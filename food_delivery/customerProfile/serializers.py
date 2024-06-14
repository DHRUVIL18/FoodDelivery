
from rest_framework import serializers
from food_delivery.customerProfile.models import CustomerProfile


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = "__all__"