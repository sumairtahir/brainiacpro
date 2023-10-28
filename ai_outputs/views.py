from django.shortcuts import render
from authentication.decorators import subscription_required
from features.models import OutputHistory, Feature
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.


@login_required(login_url='login')
@subscription_required()
def output_history(request, feature_slug):
    outputs = OutputHistory.objects.filter(user=request.user, feature__slug=feature_slug, deleted=0)
    page = 'outputs'
    context = {
        'page': page,
        'outputs': outputs
    }
    return render(request, 'outputs.html', context)


@login_required(login_url='login')
@subscription_required()
def outputs_main_view(request):

    outputs = OutputHistory.objects.filter(user=request.user, deleted=0)
    features = Feature.objects.filter(output__in=outputs).distinct()

    page = 'outputs'
    context = {
        'page': page,
        'features': features
    }

    return render(request, 'outputs_main.html', context)


@login_required(login_url='login')
@subscription_required()
def delete_output(request, output_id):

    if request.method == 'POST':
        output = OutputHistory.objects.get(id=output_id)
        output.deleted = 1
        output.save()
    
    return JsonResponse({})


    