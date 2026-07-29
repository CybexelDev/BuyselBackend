from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken


class BasicAgentBlockMiddleware:

    BLOCKED_PATHS = [
        "/api/agent/dashboard/",
        "/api/agent/property/",
        "/api/agent/property/list/",
        "/api/enquiries/",
        "/api/enquiry/",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Check only the blocked URLs
        if request.path in self.BLOCKED_PATHS:

            auth_header = request.headers.get("Authorization")

            if auth_header and auth_header.startswith("Bearer "):
                try:
                    token = auth_header.split(" ")[1]
                    decoded = AccessToken(token)

                    agent_type = decoded.get("agent_type")

                    # Block basic agents
                    if agent_type == "basic":
                        return JsonResponse(
                            {
                                "status": False,
                                "message": "Basic agents are not allowed to access this API."
                            },
                            status=403
                        )

                except Exception:
                    # Invalid token, let authentication handle it
                    pass

        response = self.get_response(request)
        return response