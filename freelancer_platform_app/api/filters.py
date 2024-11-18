from django_filters import rest_framework as filters
from ..models import Offer


class OfferFilter(filters.FilterSet):
    creator_id = filters.NumberFilter(field_name='user_id')
    min_price = filters.NumberFilter(method='filter_min_price')
    max_delivery_time = filters.NumberFilter(method='filter_max_delivery_time')

    def filter_min_price(self, queryset, name, value):
        return queryset.filter(details__price__lte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        return queryset.filter(details__delivery_time_in_days__lte=value)

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']
