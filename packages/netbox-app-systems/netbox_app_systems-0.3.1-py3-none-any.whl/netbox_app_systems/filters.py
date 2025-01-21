import strawberry_django
from .filtersets import AppSystemFilterSet, AppSystemAssignmentFilterSet
from .models import AppSystem, AppSystemAssignment

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

__all__ = (
    'PTUEventAssignmentFilter',
    'PTAppSystemAssignmentFilter',
)


@strawberry_django.filter(AppSystem, lookups=True)
@autotype_decorator(AppSystemFilterSet)
class AppSystemFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(AppSystemAssignment, lookups=True)
@autotype_decorator(AppSystemAssignmentFilterSet)
class AppSystemAssignmentFilter(BaseFilterMixin):
    pass