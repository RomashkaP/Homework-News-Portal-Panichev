import django_filters
from .models import Post
from django import forms

class PostFilter (django_filters.FilterSet):
    time_in_gt = django_filters.DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Показывать посты после: ',
        widget=forms.DateTimeInput(
            attrs={
                'type' : 'datetime-local',
                'class' : 'form-control'
            }
        )
    )
    class Meta:
        model = Post
        fields = {
            'title' : ['icontains'],
            'author__user__username' : ['iexact']
        }