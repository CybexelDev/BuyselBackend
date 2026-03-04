# import jwt
# from django.conf import settings
# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from developer.models import UserCreate
#
#
# class CustomJWTAuthentication(BaseAuthentication):
#
#     def authenticate(self, request):
#
#         auth_header = request.headers.get("Authorization")
#
#         if not auth_header:
#             return None
#
#         try:
#             token = auth_header.split(" ")[1]
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         except:
#             raise AuthenticationFailed("Invalid token")
#
#         try:
#             user = UserCreate.objects.get(id=payload["user_id"])
#         except UserCreate.DoesNotExist:
#             raise AuthenticationFailed("User not found")
#
#         return (user, None)
#
#
#
#
