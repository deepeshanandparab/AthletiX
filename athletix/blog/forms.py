from django import forms
from .models import Post, PostComment

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label='')

    class Meta:
        model = PostComment
        fields = ['comment']

class CommentUpdateForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label='')

    class Meta:
        model = PostComment
        fields = ['comment']
