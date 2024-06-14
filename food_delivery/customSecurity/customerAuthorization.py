from food_delivery.customSecurity.models import customerAuthTokens
from food_delivery.customerProfile.models import CustomerProfile
import jwt
import datetime

from django.conf import settings
from django.db.models import Q
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from common.messages import TOKEN_EXPIRED # type: ignore
from custom_security.models import  SellerAuthTokens # type: ignore
from e_commerce.settings import JWT_ALGORITHM, JWT_SECRET, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME # type: ignore
from .serializers import SellerAuthTokenSerializer, customerAuthTokenSerializer
from seller_profile.models import SellerOTP, SellerProfile # type: ignore

def save_custtomer_auth_tokens(authentication_tokens):
    auth_token_serializer = customerAuthTokenSerializer(data=authentication_tokens)
    if auth_token_serializer.is_valid():
        auth_token_serializer.save()


def get_authentication_tokens(customer):
    access_token = jwt.encode({"customer_id": customer.customer_id,
                               "email": customer.email,
                               "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.ACCESS_TOKEN_LIFETIME,
                               "type": "access"},
                              settings.JWT_SECRET,
                              algorithm=settings.JWT_ALGORITHM)

    refresh_token = jwt.encode({"customer_id": customer.customer_id,
                                "email": customer.email,
                                "exp": datetime.datetime.now(tz=datetime.timezone.utc) + settings.REFRESH_TOKEN_LIFETIME,
                                "type": "refresh"},
                               settings.JWT_SECRET,
                               algorithm=settings.JWT_ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_expiry": settings.ACCESS_TOKEN_LIFETIME,
        "refresh_token_expiry": settings.REFRESH_TOKEN_LIFETIME
    }


def customer_token_decode(token):
    try:
        claims = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)

        if not customerAuthTokens.objects.filter(Q(access_token=token) | Q(refresh_token=token)).exists():
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        if "customer_id" not in claims:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        customer = CustomerProfile.objects.get(customer_id=claims["customer_id"],
                                         email=claims["email"],
                                         is_deleted=False)

        return customer, claims

    except CustomerProfile.DoesNotExist as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)

    except AuthenticationFailed as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)

    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)
    except jwt.exceptions.InvalidSignatureError as e:
        raise AuthenticationFailed(detail=TOKEN_EXPIRED)
    except Exception as e:
        raise e


class CustomerJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
           
            if "authorization" not in request.headers:
                raise PermissionDenied()

            token = request.headers.get("authorization").split(" ")[1]

            return customer_token_decode(token)

        except PermissionDenied as e:
            raise PermissionDenied()

        except AuthenticationFailed as e:
            raise AuthenticationFailed(e.detail)

        except jwt.ExpiredSignatureError as e:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)

        except jwt.exceptions.DecodeError as e:
            raise AuthenticationFailed(detail=TOKEN_EXPIRED)
