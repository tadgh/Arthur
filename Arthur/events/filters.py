
from django_filters import rest_framework as filters

class LeaderboardFilter(filters.FilterSet):
    posted = filters.DateFromToRangeFilter(field_name='date')