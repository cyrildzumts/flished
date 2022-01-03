from django import forms
from django.contrib.auth.models import Group, Permission



class TokenForm(forms.Form):
    user = forms.IntegerField()


class GroupFormCreation(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']