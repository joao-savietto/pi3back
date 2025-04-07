import django_filters as filters
from ...users.models import User


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = User
        fields = ['email']
