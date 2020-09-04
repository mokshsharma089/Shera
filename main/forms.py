from django import forms

class GroupForm(forms.Form):
    password=forms.CharField(max_length=128)
    