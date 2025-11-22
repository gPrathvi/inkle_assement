from .models import Activity

def log_activity(actor, type, post=None, target_user_id=None):
    # Defensive helper to avoid crashing on misuse
    # type can be POST, LIKE, COMMENT, FOLLOW, BLOCK, etc.
    Activity.objects.create(actor=actor, type=type, post=post, target_user_id=target_user_id)
