from django import forms
from allauth.account.adapter import get_adapter


# from user_profile.models import Profile

class SignupForm(forms.Form):
    name = forms.CharField(max_length=100)

    def signup(self, request, user):
        adapter = get_adapter()
        username = adapter.generate_unique_username([self.cleaned_data['name']])
        user.username = username
        user.save()
