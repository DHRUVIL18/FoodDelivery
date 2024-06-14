from food_delivery.customSecurity.models import customerAuthTokens
from food_delivery.customerProfile import serializers


class customerAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = customerAuthTokens
        fields = "__all__"