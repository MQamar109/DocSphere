from django.core.cache import cache

from .models import Organization
from .serializers import OrganizationSerializer

CACHE_TTL = 60 * 10  # 10 minutes


def get_cached_organization(organization_id: int) -> dict:
    key = f"organization:{organization_id}"
    data = cache.get(key)

    if data is None:
        organization = Organization.objects.get(pk=organization_id)
        data = OrganizationSerializer(organization).data
        cache.set(key, data, CACHE_TTL)

    return data


def get_cached_organization_list() -> list:
    key = "organizations:active:list"
    data = cache.get(key)

    if data is None:
        organizations = Organization.objects.filter(is_active=True)
        data = OrganizationSerializer(organizations, many=True).data
        cache.set(key, data, CACHE_TTL)

    return data


def invalidate_organization_cache(organization_id: int):
    cache.delete(f"organization:{organization_id}")
    cache.delete("organizations:active:list")
