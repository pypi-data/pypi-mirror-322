from . import filters, models
from typing import Annotated, List
import strawberry
import strawberry_django
from django.contrib.contenttypes.models import ContentType


# PTContentTypeType (для ContentType, используемое в GenericForeignKey)
@strawberry_django.type(
    model=ContentType,
    fields="__all__",
)
class PTContentTypeType:
    pass


@strawberry_django.type(
    model = models.AppSystem,
    fields="__all__",
)
class AppSystemType:
    pass


@strawberry_django.type(
    model = models.AppSystemAssignment,
    fields="__all__",
    filters=filters.AppSystemAssignmentFilter,
)
class AppSystemAssignmentType:
    object_type: Annotated["PTContentTypeType", strawberry_django.field()]  # Внешний ключ на ContentType
    object: Annotated[str, strawberry_django.field()]
    app_system: Annotated["AppSystemType", strawberry_django.field()]  # Внешний ключ на AppSystem


@strawberry.type
class Query:

    @strawberry.field
    def app_system(self, id: int) -> AppSystemType:
        return models.AppSystem.objects.get(pk=id)
    
    app_system_list: List[AppSystemType] = strawberry_django.field()

    @strawberry.field
    def app_system_assignment(self, id: int) -> AppSystemAssignmentType:
        return models.AppSystemAssignment.objects.get(pk=id)
    
    app_system_assignment_list: List[AppSystemAssignmentType] = strawberry_django.field()

schema = [Query]
