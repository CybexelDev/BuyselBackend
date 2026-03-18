# agents/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .models import AgentUserProfile

class AgentJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            decoded = AccessToken(token)

            # 🔥 get username instead of id
            username = decoded.get("username")

            if not username:
                raise AuthenticationFailed("Invalid token")

            agent = AgentUserProfile.objects.filter(username=username).first()

            if not agent:
                raise AuthenticationFailed("Agent not found")

            return (agent, None)

        except Exception as e:
            raise AuthenticationFailed("Invalid token")