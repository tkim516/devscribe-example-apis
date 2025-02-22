from rest_framework.views import APIView
from rest_framework.response import Response

class UserView(APIView):
    def get(self, request):
        """Get all users."""
        return Response([{"id": 1, "name": "Alice"}])

    def post(self, request):
        """Create a user."""
        return Response({"id": 2, "name": request.data.get("name", "New User")})