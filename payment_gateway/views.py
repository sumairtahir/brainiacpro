import json
import stripe
import secrets
import pytz
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Product, Subscription
from django.contrib.auth.decorators import login_required
from datetime import datetime
from dateutil.relativedelta import relativedelta

stripe.api_key = settings.STRIPE_SECRET_KEY


def success_view(request):
    subscription_id = request.GET.get('subscription_id', None)
    access_token = request.GET.get('access_token', None)
    print(request.user)
    subscription = Subscription.objects.filter(id=subscription_id).first()

    if subscription and access_token == subscription.token:
        if not subscription.is_completed:

            previous_subscription = Subscription.objects.filter(user=request.user, is_expired=0, is_completed=1).first()
            tokens_left = request.user.tokens
            if previous_subscription:
                previous_subscription.is_expired = 1
                current = pytz.utc.localize(datetime.now())
                remaining_days = (previous_subscription.expiry - current).days - 1
                tokens_left = int(tokens_left/(30 - remaining_days))
                previous_subscription.save()
            
            subscription.is_completed = 1
            request.user.tokens = tokens_left + subscription.product.tokens
            subscription.tokens = subscription.product.tokens + tokens_left
            request.user.save()
            subscription.save()
            
    else:
        return HttpResponse('401 Unauthorized')

    context = {
        'subscription': subscription
    }

    return render(request, 'success.html', context)


class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):

        previous_subscription = Subscription.objects.filter(user=request.user, is_expired=0).first()
        upgrade_consent = request.GET.get('consent', 0)
        
        tokens_left = request.user.tokens
        if previous_subscription and tokens_left != 0 and not upgrade_consent:
            if previous_subscription.is_expirable:
                remaining_days = previous_subscription.expiry
                current = pytz.utc.localize(datetime.now())
                remaining_days = (previous_subscription.expiry - current).days - 1
                tokens_left = int(tokens_left/(30 - int(remaining_days)))

            return JsonResponse({'tokens_left': tokens_left, 'status': 300})       

        token = secrets.token_hex(32)
        request.session['access_token'] = token
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://localhost:8080"

        subscription = Subscription(
            user=request.user,
            product=product,
            price=product.price,
            is_expirable=product.is_expirable,
            token=token
        )

        if subscription.is_expirable:
            subscription.expiry = datetime.now() + relativedelta(months=+1)

        subscription.save()

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "subscription_id": subscription.id,
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success?subscription_id=' + str(subscription.id) + '&access_token=' + token,
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        subscription_id = session["metadata"]["subscription_id"]

        subscription = Subscription.objects.get(id=subscription_id)
        subscription.is_verified = 1
        subscription.save()


    return HttpResponse(status=200)