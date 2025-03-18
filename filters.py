import django_filters
from .models import Course, Student


class CourseFilter(django_filters.FilterSet):
    teacher = django_filters.CharFilter(field_name="teacher__user__username", lookup_expr="icontains")
    tags = django_filters.CharFilter(method='filter_by_tags')
    start_date = django_filters.DateFilter(field_name="start_date", lookup_expr="gte")

    class Meta:
        model = Course
        fields = ['teacher', 'tags', 'start_date']

    def filter_by_tags(self, queryset, name, value):
        tags = value.split(',')
        return queryset.filter(tags__overlap=tags)

class StudentFilter(django_filters.FilterSet):
    min_points = django_filters.NumberFilter(field_name="points", lookup_expr="gte")
    max_points = django_filters.NumberFilter(field_name="points", lookup_expr="lte")

    class Meta:
        model = Student
        fields = ['course', 'min_points', 'max_points']