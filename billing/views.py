from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import stripe
from .models import UserPayment
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from core.settings import STRIPE_SECRET_KEY


# Create your views here.
stripe.api_key = STRIPE_SECRET_KEY

@login_required(login_url='login')
def product_page(request):
    if request.method == 'POST':
        price_id = 'price_1ORKbZKwogVwbigBp6kztRUt'  # Replace with your actual price ID
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                }
            ],
            mode='subscription',
            success_url = 'http://localhost:8000/billing' + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('payment_cancelled'))
        )
        return redirect(checkout_session.url, code=303)
    return render(request, 'product_page.html')


## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
	stripe.api_key = STRIPE_SECRET_KEY
	checkout_session_id = request.GET.get('session_id', None)
	session = stripe.checkout.Session.retrieve(checkout_session_id)
	customer = stripe.Customer.retrieve(session.customer)
	user_id = request.user
	user_payment = UserPayment.objects.get(app_user=user_id)
	user_payment.stripe_checkout_id = checkout_session_id
	user_payment.save()
	return render(request, 'payment_succes.html', {'customer': customer})


def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    signature_header = request.headers['Stripe-Signature']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, STRIPE_SECRET_KEY
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()

    return HttpResponse(status=200)
