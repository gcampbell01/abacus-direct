from django.forms import ModelForm
from django import forms

class CustomMessageForm(forms.Form):
    sender_name = forms.CharField(widget=forms.TextInput( attrs={'placeholder': 'Your Name'}))
    sender_email = forms.EmailField(widget=forms.TextInput( attrs={'placeholder': 'Your Email'}))
    subject = forms.CharField(widget=forms.TextInput( attrs={'placeholder': 'Subject'}))
    body = forms.CharField(widget=forms.Textarea( attrs={'placeholder': 'Your Message'}))

