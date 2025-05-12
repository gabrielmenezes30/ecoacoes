from django import forms
from .models import Group, GroupMembership

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'city', 'avatar']

class InviteForm(forms.Form):
    email = forms.EmailField(required=False)
    invite_code = forms.CharField(max_length=20, required=False)