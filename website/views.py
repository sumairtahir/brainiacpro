from django.shortcuts import render

# Create your views here.


def home(request):
    '''
    Website Landing Page
    '''

    return render(request, 'index.html', {})


def pricing(request):
    '''
    Website Landing Page
    '''

    return render(request, 'pricing.html', {})
