from . import models
from django import forms

class Post_form(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }

class Comment_form(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('author','text')

        widgets ={
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea '}),
        }