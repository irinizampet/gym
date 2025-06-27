from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MemberSignupForm


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

def payment_view(request):
    return render(request, 'payment.html')

def signup_view(request):
    if request.method == 'POST':
        form = MemberSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        # αν δεν είναι valid, θα περάσει ξανά στο render με τα form.errors
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
    return render(request, 'index.html') 

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

def booking_view(request):
    return render(request, 'booking.html')

def history_view(request):
    return render(request, 'training-history.html')

def announcements_view(request):
    return render(request, 'announcement.html')

def profil_view(request):
    return render(request, 'profil.html')

#@login_required
# def payment_view(request):
#     # 1) Υπολογισμός ήδη αγορασμένων εισόδων μέσω Payments
#     purchased = (
#         Payment.objects
#                .filter(user=request.user)
#                .aggregate(total=Sum('sub__avail_participations'))['total']
#         or 0
#     )

#     # 2) Φόρτωση διαθέσιμων πακέτων + υπολογισμός κόστους
#     subscriptions = list(Subscription.objects.all())
#     for sub in subscriptions:
#         sub.cost = sub.avail_participations * PRICE_PER_SESSION

#     error = None
#     selected = None

#     # 3) Επεξεργασία φόρμας
#     if request.method == 'POST':
#         selected = request.POST.get('sub_id')
#         if not selected:
#             error = "Πρέπει να επιλέξεις ένα πακέτο."
#         else:
#             sub = get_object_or_404(Subscription, pk=selected)
#             Payment.objects.create(
#                 user=request.user,
#                 sub=sub,
#                 amount=sub.cost,
#                 tran_date=timezone.now()
#             )
#             return redirect('profile')

#     # 4) Απόδοση template
#     return render(request, 'payment.html', {
#         'subscriptions': subscriptions,
#         'purchased':     purchased,
#         'error':         error,
#         'selected':      selected,
#     })
