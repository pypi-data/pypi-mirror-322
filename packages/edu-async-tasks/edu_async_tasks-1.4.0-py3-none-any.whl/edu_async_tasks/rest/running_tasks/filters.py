from django_filters import (
    rest_framework as filters,
)

from edu_async_tasks.core.models import (
    RunningTask,
)


class RunningTasksFilter(filters.FilterSet):

    queued_at_from = filters.DateFilter(field_name='queued_at', lookup_expr='date__gte', label='Дата с')
    queued_at_to = filters.DateFilter(field_name='queued_at', lookup_expr='date__lte', label='Дата по')
    queued_at = filters.DateFilter(lookup_expr='date')
    started_at = filters.DateFilter(lookup_expr='date')
    finished_at = filters.DateFilter(lookup_expr='date')

    ordering = filters.OrderingFilter(
        fields=(
            ('queued_at', 'queued_at'),
            ('description', 'description'),
            ('status__title', 'status'),
            ('execution_time', 'execution_time'),
        )
    )

    class Meta:
        model = RunningTask
        fields = (
            'queued_at',
            'started_at',
            'finished_at',
            'name',
            'status',
        )
