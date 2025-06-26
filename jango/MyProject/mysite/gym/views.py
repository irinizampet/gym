from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Subscription, Payment, History


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

import random
from django.contrib import messages
from .forms import PasswordResetForm
from django.contrib.auth.hashers import make_password

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            member = Member.objects.get(email=email)

            # Νέος προσωρινός κωδικός (ή βάλε σταθερό: 'newpass123')
            new_password = f"newpass{random.randint(1000, 9999)}"
            member.password = make_password(new_password)
            member.save()

            messages.success(request, f"Ο νέος σας κωδικός είναι: {new_password}")
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'passreset.html', {'form': form})

from .models import Member

@login_required(login_url='login')
def dashboard_view(request):
    member = Member.objects.get(username=request.user.username)
    return render(request, 'περιβαλλονχρηστη.html', {'member': member})

def index_view(request):
    return render(request, 'index.html')  # ή το αρχικό σου template

def filosofia_view(request):
    return render(request, 'filosofia.html')

def contact_view(request):
    return render(request, 'contact.html')

def Programmata_view(request):
    return render(request, 'Πρόγραμμα.html')

def προπονητες_view(request):
    return render(request, 'Προπονητές.html')

def profil_view(request):
    return render(request, 'profil.html')

def krathsh_view(request):
    return render(request, 'Κράτηση.html')

def history_view(request):
    return render(request, 'training-history.html')

def announcements_view(request):
    return render(request, 'announcement.html')

def profil_view(request):
    return render(request, 'profil.html')

from django.shortcuts    import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models    import Sum
from .models             import Subscription, Payment, History

PRICE_PER_SESSION = 10

@login_required
def payment_view(request):
    # Υπολογισμός ήδη αγορασμένων εισόδων
    purchased = (
        Payment.objects
               .filter(user=request.user)
               .aggregate(total=Sum('subscription__avail_participations'))['total']
        or 0
    )
    # Φόρτωση πακέτων και υπολογισμός κόστους ΣΕ ΚΑΘΕ sub
    subscriptions = list(Subscription.objects.all())
    for sub in subscriptions:
        sub.cost = sub.avail_participations * PRICE_PER_SESSION

    error = None
    selected = None

    if request.method == 'POST':
        selected = request.POST.get('sub_id')
        if not selected:
            error = "Πρέπει να επιλέξεις ένα πακέτο."
        else:
            sub = get_object_or_404(Subscription, pk=selected)
            Payment.objects.create(
                user=request.user,
                subscription=sub,
                amount=sub.cost
            )
            return redirect('profile')

    return render(request, 'payment.html', {
        'subscriptions': subscriptions,
        'purchased': purchased,
        'error': error,
        'selected': selected,
    })
