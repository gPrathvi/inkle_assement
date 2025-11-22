from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from .models import User
from .serializers import SignupSerializer, UserSerializer
from .permissions import IsOwnerRole

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]  # allow signup without auth

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        user = request.user
        from .serializers import ProfileUpdateSerializer
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(user).data)

class PromoteAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerRole]

    def post(self, request, user_id):
        try:
            u = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        u.role = User.ROLE_ADMIN
        u.save()
        return Response({"detail": "Promoted to admin"})

class DemoteAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerRole]

    def delete(self, request, user_id):
        try:
            u = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        u.role = User.ROLE_USER
        u.save()
        return Response({"detail": "Demoted to user"})

class UserSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        if not q:
            return Response({'count': 0, 'results': []})
        qs = User.objects.filter(
            models.Q(username__icontains=q) | models.Q(email__icontains=q)
        ).order_by('username')
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        items = qs[offset:offset+limit]
        data = [
            {'id': u.id, 'username': u.username, 'email': u.email, 'role': u.role}
            for u in items
        ]
        return Response({'count': qs.count(), 'results': data})

# Create your views here.
