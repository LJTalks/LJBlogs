from .models import BlogComment
from django import forms


class BlogCommentForm(forms.ModelForm):

    class Meta:
        model = BlogComment
        fields = ('body',)
        labels = {
            'body': '',  # Removes the label
        }