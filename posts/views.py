from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrAdmin, IsCommentAuthorOrAdmin
from activities.utils import log_activity

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(is_deleted=False).annotate(likes_count=Count("likes"))

    def get_permissions(self):
        # Apply object-level author/admin checks only to write operations on an object
        if self.action in {"update", "partial_update", "destroy"}:
            from .permissions import IsAuthorOrAdmin
            return [permissions.IsAuthenticated(), IsAuthorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        log_activity(actor=self.request.user, type="POST", post=post)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        # soft delete
        post.is_deleted = True
        post.save(update_fields=["is_deleted"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post", "delete"], url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        if request.method == "POST":
            obj, created = Like.objects.get_or_create(user=request.user, post=post)
            if created:
                log_activity(actor=request.user, type="LIKE", post=post)
                # Notify the post author
                from activities.models import Notification
                if post.author_id != request.user.id:
                    Notification.objects.create(recipient_id=post.author_id, actor=request.user, type="LIKE", post=post)
                return Response({"detail": "liked"}, status=status.HTTP_201_CREATED)
            return Response({"detail": "already liked"}, status=status.HTTP_200_OK)
        # DELETE
        Like.objects.filter(user=request.user, post=post).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Comment.objects.filter(is_deleted=False)
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def get_permissions(self):
        if self.action in {"update", "partial_update", "destroy"}:
            return [permissions.IsAuthenticated(), IsCommentAuthorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        log_activity(actor=self.request.user, type="COMMENT", post=comment.post)
        # Notify the post author
        from activities.models import Notification
        if comment.post.author_id != self.request.user.id:
            Notification.objects.create(recipient_id=comment.post.author_id, actor=self.request.user, type="COMMENT", post=comment.post)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.is_deleted = True
        comment.save(update_fields=["is_deleted"])
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
