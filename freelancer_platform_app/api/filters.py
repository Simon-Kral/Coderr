from django_filters import rest_framework as filters
from ..models import Offer


class OfferFilter(filters.FilterSet):
    """
    Custom filter class for filtering offers based on various criteria.

    Filters:
        - creator_id: Filters offers by the ID of the user who created them.
        - min_price: Filters offers where the minimum price of their details is less than or equal to a specified value.
        - max_delivery_time: Filters offers where the maximum delivery time of their details is less than or equal to a specified value.
    """

    creator_id = filters.NumberFilter(field_name='user_id')
    min_price = filters.NumberFilter(method='filter_min_price')
    max_delivery_time = filters.NumberFilter(method='filter_max_delivery_time')

    def filter_min_price(self, queryset, name, value):
        """
        Filters the queryset to include offers with at least one detail 
        having a price less than or equal to the specified value.
        """
        return queryset.filter(details__price__lte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        """
        Filters the queryset to include offers with at least one detail 
        having a delivery time less than or equal to the specified value.
        """
        return queryset.filter(details__delivery_time_in_days__lte=value)

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']
