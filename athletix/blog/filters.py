from django.forms import TextInput
from .models import Post
import django_filters

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains',
                                      widget=TextInput
                                        (
                                          attrs={
                                              'placeholder': 'Enter Title',
                                              'autocomplete' : 'false',
                                              'class': 'form form-control mb-2'
                                                 }),label='Post Title')

    class Meta:
        model = Post
        fields = ['title']