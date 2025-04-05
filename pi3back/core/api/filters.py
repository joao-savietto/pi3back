import django_filters as filters
from ..models import Occurrence
from ...users.models import User

class OccurrenceFilter(filters.FilterSet):
    student = filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = Occurrence
        fields = ['student']

class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = User
        fields = ['email']