from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import Account
from authentication.decorators import subscription_required
from features.models import OutputHistory, FavoriteFeature
from payment_gateway.models import Subscription
from django.db.models import Sum

# Create your views here.


@login_required(login_url='login')
@subscription_required()
def profile_view(request):

    user = request.user

    words_count = 0
    subscription = Subscription.objects.filter(user=request.user, is_expired=0, is_completed=1).first()
    if subscription:
        words_count = subscription.tokens
    usage = words_count - request.user.tokens

    total_words_generated = OutputHistory.objects.values('tokens').filter(user=request.user).aggregate(Sum('tokens'))['tokens__sum']
    total_fav_features = FavoriteFeature.objects.filter(user=request.user).count()

    if request.method == "POST":
        
        if 'edit_profile' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            company = request.POST.get('company')
            address_line_1 = request.POST.get('address_line_1')
            address_line_2 = request.POST.get('address_line_2')
            phone_number = request.POST.get('phone_number')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')

            if 'profile_pic' in request.FILES:
                user.profile_picture = request.FILES['profile_pic']

            user.first_name = first_name
            user.last_name = last_name
            user.company = company
            user.address_line_1 = address_line_1
            user.address_line_2 = address_line_2
            user.phone_number = phone_number
            user.city = city
            user.state = state
            user.country = country
            user.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('/profile')

    context = {}

    context['words_count'] = words_count
    context['total_words_generated'] = total_words_generated
    context['total_fav_features'] = total_fav_features
    context['usage'] = usage
    context['page'] = 'profile'

    return render(request, 'user_profile.html', context)


@login_required(login_url='login')
@subscription_required()
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('account')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('account')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('account')
    return render(request, 'change_password.html',  {'page': 'change_password'})


@login_required(login_url='login')
@subscription_required()
def billing_view(request):

    words_count = 0
    subscription = Subscription.objects.filter(user=request.user, is_expired=0, is_completed=1).first()
    if subscription:
        words_count = subscription.tokens
    usage = words_count - request.user.tokens

    total_words_generated = OutputHistory.objects.values('tokens').filter(user=request.user).aggregate(Sum('tokens'))['tokens__sum']
    total_fav_features = FavoriteFeature.objects.filter(user=request.user).count()

    context = {}
    context['words_count'] = words_count
    context['total_words_generated'] = total_words_generated
    context['total_fav_features'] = total_fav_features
    context['usage'] = usage
    context['page'] = 'billing'

    return render(request, 'billing.html',  context)