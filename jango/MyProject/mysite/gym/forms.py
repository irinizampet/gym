from django import forms
from .models import Member
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class MemberSignupForm(forms.Form):
    name             = forms.CharField(max_length=30, label="Όνομα")
    surname          = forms.CharField(max_length=30, label="Επώνυμο")
    phone_num        = forms.CharField(max_length=15, label="Τηλέφωνο")
    email            = forms.EmailField(label="Email")
    username         = forms.CharField(max_length=20, label="Όνομα χρήστη")
    password         = forms.CharField(min_length=8, widget=forms.PasswordInput, label="Κωδικός")
    password_confirm = forms.CharField(min_length=8, widget=forms.PasswordInput, label="Επιβεβαίωση Κωδικού")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                f"Το όνομα χρήστη «{username}» χρησιμοποιείται ήδη."
            )
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f"Το email «{email}» χρησιμοποιείται ήδη σε άλλο λογαριασμό."
            )
        if Member.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f"Το email «{email}» χρησιμοποιείται ήδη σε άλλο μέλος."
            )
        return email

    def clean_phone_num(self):
        phone = self.cleaned_data['phone_num']
        
        normalized = ''.join(ch for ch in phone if ch.isdigit())
        if Member.objects.filter(phone_num__iexact=normalized).exists():
            raise forms.ValidationError(
                f"Ο αριθμός τηλεφώνου «{phone}» χρησιμοποιείται ήδη."
            )
        
        return normalized

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get("password")
        pw2 = cleaned.get("password_confirm")
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError("Οι κωδικοί δεν ταιριάζουν.")
        return cleaned

    def save(self):
        data = self.cleaned_data
        
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        member = Member(
            name      = data['name'],
            surname   = data['surname'],
            phone_num = data['phone_num'],  
            email     = data['email'],
            username  = data['username'],
            password  = user.password
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