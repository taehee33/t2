from django import forms

from .models import Post, Comment

#from wtforms_django.orm import Form, TextField, TextAreaField, validators, StringField, SubmitField







class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

'''

class ReusableForm(Form):
    dataname = TextField('Name:', validators=[validators.required(),
    validators.Length(min=4, max=100)])
    '''
class ContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required = True , min_length=4, max_length=100)


'''

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    '''
