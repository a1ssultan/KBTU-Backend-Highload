from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Comment


@receiver(post_save, sender=Comment)
def invalidate_comment_count_cache_on_adding(sender, instance, **kwargs):
    cache_key = f'comment_count_{instance.post.id}'
    cache.delete(cache_key)


@receiver(post_delete, sender=Comment)
def invalidate_comment_count_cache_on_deleting(sender, instance, **kwargs):
    cache_key = f'comment_count_{instance.post.id}'
    cache.delete(cache_key)
