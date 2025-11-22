from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Follow, Block
from activities.utils import log_activity


def is_blocked(a_id, b_id):
    # True if either user has blocked the other
    return Block.objects.filter(blocker_id=a_id, blocked_id=b_id).exists() or Block.objects.filter(blocker_id=b_id, blocked_id=a_id).exists()


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if user_id == request.user.id:
            return Response({"detail": "Cannot follow yourself"}, status=400)
        if is_blocked(request.user.id, user_id):
            return Response({"detail": "Blocked"}, status=403)
        obj, created = Follow.objects.get_or_create(follower_id=request.user.id, followee_id=user_id)
        log_activity(actor=request.user, type="FOLLOW", target_user_id=user_id)
        # Create notification for the followed user
        from activities.models import Notification
        if created and user_id != request.user.id:
            Notification.objects.create(recipient_id=user_id, actor=request.user, type="FOLLOW")
        return Response({"detail": "followed"})

    def delete(self, request, user_id):
        Follow.objects.filter(follower_id=request.user.id, followee_id=user_id).delete()
        return Response({"detail": "unfollowed"})


class BlockView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if user_id == request.user.id:
            return Response({"detail": "Cannot block yourself"}, status=400)
        Block.objects.get_or_create(blocker_id=request.user.id, blocked_id=user_id)
        Follow.objects.filter(follower_id=request.user.id, followee_id=user_id).delete()
        Follow.objects.filter(follower_id=user_id, followee_id=request.user.id).delete()
        return Response({"detail": "blocked"})

    def delete(self, request, user_id):
        Block.objects.filter(blocker_id=request.user.id, blocked_id=user_id).delete()
        return Response({"detail": "unblocked"})

# Create your views here.
