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
            messages.error(request, 'Λάθος όνομα χρήστη ή κωδικός.')
    return render(request, 'login.html')
