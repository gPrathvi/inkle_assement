from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Q
from .models import Activity, Notification
from social.models import Follow, Block

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        following_ids = Follow.objects.filter(follower_id=user.id).values_list("followee_id", flat=True)
        blocked_ids = set(Block.objects.filter(blocker_id=user.id).values_list("blocked_id", flat=True)) | set(Block.objects.filter(blocked_id=user.id).values_list("blocker_id", flat=True))
        actors = [user.id] + [uid for uid in following_ids if uid not in blocked_ids]
        qs = Activity.objects.filter(actor_id__in=actors).exclude(Q(actor_id__in=blocked_ids) | Q(target_user_id__in=blocked_ids))
        t = request.query_params.get("type")
        if t == "posts":
            qs = qs.filter(type="POST")
        elif t == "likes":
            qs = qs.filter(type="LIKE")
        elif t == "follows":
            qs = qs.filter(type="FOLLOW")
        limit = int(request.query_params.get("limit", 20))
        offset = int(request.query_params.get("offset", 0))
        items = qs[offset:offset + limit]
        data = [
            {
                "id": a.id,
                "type": a.type,
                "actor_id": a.actor_id,
                "target_user_id": a.target_user_id,
                "post_id": a.post_id,
                "created_at": a.created_at,
            }
            for a in items
        ]
        return Response({"count": qs.count(), "results": data})

class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Notification.objects.filter(recipient_id=request.user.id).order_by('-created_at')
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        items = qs[offset:offset+limit]
        data = [
            {
                'id': n.id,
                'type': n.type,
                'actor_id': n.actor_id,
                'post_id': n.post_id,
                'is_read': n.is_read,
                'created_at': n.created_at,
            }
            for n in items
        ]
        return Response({'count': qs.count(), 'results': data})

    def post(self, request):
        # Mark all as read
        Notification.objects.filter(recipient_id=request.user.id, is_read=False).update(is_read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

class NotificationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notif_id):
        # Mark single as read
        try:
            n = Notification.objects.get(id=notif_id, recipient_id=request.user.id)
        except Notification.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)
        n.is_read = True
        n.save(update_fields=['is_read'])
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
