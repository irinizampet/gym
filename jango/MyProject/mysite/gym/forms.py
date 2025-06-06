from django import forms
from .models import Member
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class MemberSignupForm(forms.Form):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    phone_num = forms.CharField(max_length=15)
    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Επιβεβαίωση Κωδικού")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Οι κωδικοί δεν ταιριάζουν.")
        return cleaned_data

    def save(self):
        data = self.cleaned_data

    # Δημιουργία Django User
        user = User.objects.create_user(
          username=data['username'],
          email=data['email'],
          password=data['password']
       )

    # Δημιουργία του Member (αν θες, μπορείς να κρατήσεις reference στον user)
        member = Member(
          name=data['name'],
          surname=data['surname'],
          phone_num=data['phone_num'],
          email=data['email'],
          username=data['username'],
          password=user.password  # hashed password από τον Django User
        )
        member.save()
        return member

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email")

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Member.objects.filter(email=email).exists():
            raise forms.ValidationError("Δεν βρέθηκε χρήστης με αυτό το email.")
        return email