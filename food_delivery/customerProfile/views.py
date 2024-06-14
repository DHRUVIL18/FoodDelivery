from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class Registration(APIView):

    @staticmethod
    def post(request):
        registration_serializer = RegistrationSerializer(data=request.data)