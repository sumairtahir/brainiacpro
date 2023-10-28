from django.shortcuts import redirect
from payment_gateway.models import Subscription


def subscription_required():
    """
    Checks if user has subscribed the plans.
    """

    def decorator(view_func):

        def wrapper_func(request, *args, **kwargs):
            subscriptions = Subscription.objects.filter(user=request.user, is_completed=1)
            active_subscription = Subscription.objects.filter(user=request.user, is_expired=0, is_completed=1)

            if not subscriptions:
                return redirect('/get-started')
            elif not active_subscription:
                request.session['active_subscription'] = 0
                return view_func(request, *args, **kwargs)
            else:
                request.session['active_subscription'] = 1
                return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator
