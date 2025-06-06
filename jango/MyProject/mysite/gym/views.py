from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('περιβαλλονχρηστη')  # άλλαξέ το με το όνομα της σελίδας μετά το login
        else:
            messages.error(request, 'Λάθος στοιχεία σύνδεσης')
    return render(request, 'login.html')

def dashboard_view(request):
    return render(request, 'περιβαλλονχρηστη.html') 

from .forms import MemberSignupForm

def signup_view(request):
    if request.method == 'POST':
        form = MemberSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # αφού γίνει η εγγραφή, τον στέλνεις στη login σελίδα
    else:
        form = MemberSignupForm()
    return render(request, 'signup.html', {'form': form})

