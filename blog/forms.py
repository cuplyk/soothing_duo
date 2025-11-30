# blog/forms.py

from django import forms
from .models import Post, Comment
from tinymce.widgets import TinyMCE

class CommentForm(forms.ModelForm):
    """
    Form for users to create a new comment on a post.
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500 mb-3',
                'placeholder': 'Your Name (Optional)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500 mb-3',
                'placeholder': 'Your Email (Optional)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500', 
                'rows': '3',
                'placeholder': 'Share your thoughts...'
            })
        }


class PostForm(forms.ModelForm):
    """
    Form for creating and editing a blog post.
    """

    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'status',"tags"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500',
                'placeholder': 'Enter a catchy title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500', 
                'rows': '10',
                'placeholder': 'Write your post content here...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500'
            }),
        }
