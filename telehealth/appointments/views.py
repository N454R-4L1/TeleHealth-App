import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm, AppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Appointment
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('home')
    else:
        form = AppointmentForm()
    return render(request, 'schedule_appointment.html', {'form': form})

@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments/view_appointments.html', {'appointments': appointments})

@login_required
def chat(request):
    return render(request, 'chat.html')

@login_required
def video_call(request):
    return render(request, 'video_call.html')

@login_required
def checkout(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        
        # You would typically save this information to your database here

        # Amount to be charged (in cents)
        amount = 5000  # $50.00

        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=email,  # Associate the payment with the email provided
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Telehealth Consultation',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return redirect(checkout_session.url, code=303)

    return render(request, 'checkout.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"Payment successful for session {session['id']}")

    return JsonResponse({'status': 'success'})
