from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class AdminListUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not (hasattr(request.user, 'is_admin') and request.user.is_admin()):
            return Response({"detail": "Forbidden"}, status=403)
        qs = User.objects.all().order_by('username')
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))
        items = qs[offset:offset+limit]
        data = [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'role': u.role,
                'is_active': u.is_active,
            } for u in items
        ]
        return Response({'count': qs.count(), 'results': data})

class AdminDeactivateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        if not (hasattr(request.user, 'is_admin') and request.user.is_admin()):
            return Response({"detail": "Forbidden"}, status=403)
        try:
            u = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        u.is_active = False
        u.save(update_fields=['is_active'])
        return Response({"detail": "user deactivated"})

class AdminReactivateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if not (hasattr(request.user, 'is_admin') and request.user.is_admin()):
            return Response({"detail": "Forbidden"}, status=403)
        try:
            u = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        u.is_active = True
        u.save(update_fields=['is_active'])
        return Response({"detail": "user reactivated"})

class AdminDeletePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        if not (hasattr(request.user, 'is_admin') and request.user.is_admin()):
            return Response({"detail": "Forbidden"}, status=403)
        try:
            p = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=404)
        p.is_deleted = True
        p.save()
        return Response({"detail": "post deleted"})

# Create your views here.
