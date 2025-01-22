from django_filters import rest_framework as filters

from . import models


class Ticket(filters.FilterSet):
    user_id = filters.NumberFilter(
        field_name='user',
        lookup_expr='exact',
    )

    class Meta:
        model = models.Ticket
        fields = [
            'user_id',
            'resolved',
        ]
