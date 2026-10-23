
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from agents.models import AgentUserProfile, SecretUser
from users.models import UserCreate


class UnifiedAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed("Invalid authorization header.")

        try:
            token = AccessToken(parts[1])
        except Exception:
            raise AuthenticationFailed("Invalid or expired token.")

        # 1. Secret user authentication
        if token.get("role") == "secret_user":
            secret_user = SecretUser.objects.filter(
                id=token.get("user_id"),
                is_active=True
            ).select_related("agent").first()

            if not secret_user:
                raise AuthenticationFailed("Secret user not found.")

            agent = secret_user.agent

            if (
                not agent.is_active
                or not agent.is_company_agent
                or not agent.secret_properties
            ):
                raise AuthenticationFailed("Secret user access is disabled.")

            return (secret_user, token)

        # 2. Agent authentication
        agent_code = token.get("agent_code")

        if agent_code:
            agent = AgentUserProfile.objects.filter(
                agent_code=agent_code,
                username=token.get("username")
            ).first()

            if not agent:
                raise AuthenticationFailed("Agent not found.")

            if not agent.is_active:
                raise AuthenticationFailed("Agent account is inactive.")

            return (agent, token)

        # 3. Normal user authentication
        user_id = token.get("user_id")

        if user_id:
            user = UserCreate.objects.filter(id=user_id).first()

            if user:
                return (user, token)

        raise AuthenticationFailed("Unable to authenticate this token.")
