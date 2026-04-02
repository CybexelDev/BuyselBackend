from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserCreate

class UserJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token["user_id"]
            user = UserCreate.objects.get(id=user_id)
            return user
        except UserCreate.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")