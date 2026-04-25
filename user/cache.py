from django.core.cache import cache
from user.models import User
from user.serializers import ListDetailUserSerializer

CACHE_TTL = 60 * 10  


def get_cached_user(user_id: int) -> dict:
    key = f"user:{user_id}"
    data = cache.get(key)

    if data is None:
        user = User.objects.prefetch_related(
            'project_permissions__project',
            'document_permissions__document',
        ).get(pk=user_id)
        data = ListDetailUserSerializer(user).data
        cache.set(key, data, CACHE_TTL)

    return data


def get_cached_user_list() -> list:
    key = "users:active:list"
    data = cache.get(key)

    if data is None:
        users = User.objects.prefetch_related(
            'project_permissions__project',
            'document_permissions__document',
        ).filter(is_active=True)
        data = ListDetailUserSerializer(users, many=True).data
        cache.set(key, data, CACHE_TTL)

    return data


def invalidate_user_cache(user_id: int):
    cache.delete(f"user:{user_id}")
    cache.delete("users:active:list")