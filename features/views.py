'''Features'''

import http
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from authentication.decorators import subscription_required
from features.DeClutter import DeClutter
from features.models import OutputHistory, Feature, FavoriteFeature, Category
from utils.helpers import count_words


@login_required(login_url='login')
@subscription_required()
def dashboard_view(request):

    fav_features = request.user.favorite_features.filter(is_fav=1)
    print(fav_features)
    context = {
        'page': 'dashboard',
        'fav_features': fav_features
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@subscription_required()
def features(request):
    '''
    App Features Page
    '''

    features = Feature.objects.all()
    categories = Category.objects.all()

    for feature in features:
        fav_features = request.user.favorite_features.values_list(
            'feature_id', flat=True).filter(is_fav=1)

        if feature.id in fav_features:
            feature.is_fav = 1

    page = 'features'
    context = {
        'page': page,
        'features': features,
        'categories': categories
    }

    return render(request, 'features.html', context)


def save_output(output, model, feature, user):
    word_count = count_words(output)
    output_history_obj = OutputHistory(
        user=user,
        output=output,
        model=model,
        tokens=word_count,
        feature=feature,
    )
    output_history_obj.save()

    user.tokens = user.tokens - int(word_count * 1.0)
    user.save()

    return output_history_obj.id


@login_required(login_url='login')
@subscription_required()
def star_output(request, output_id):

    if request.method == 'POST':
        output = OutputHistory.objects.get(id=output_id)
        if output.stared == 0:
            output.stared = 1
        else:
            output.stared = 0
        output.save()

    return JsonResponse({'output': output.stared})


@login_required(login_url='login')
@subscription_required()
def favorite_feature_view(request, feature_id):

    if request.method == 'POST':
        fav_feature = FavoriteFeature.objects.filter(
            feature_id=feature_id, user=request.user).first()

        if not fav_feature:
            fav_feature = FavoriteFeature(
                feature_id=feature_id,
                user=request.user,
                is_fav=0,
            )
            fav_feature.save()

        if fav_feature.is_fav == 0:
            fav_feature.is_fav = 1
        else:
            fav_feature.is_fav = 0
        fav_feature.save()

    return JsonResponse({'output': fav_feature.is_fav})


@login_required(login_url='login')
@subscription_required()
def document_mode(request, task):
    '''Boss Mode'''
    context = {}

    return render(request, 'document-mode.html', context)


@login_required(login_url='login')
@subscription_required()
def feature_view(request, feature_slug):
    '''
    Features.
    '''

    feature = Feature.objects.get(slug=feature_slug)

    if request.method == 'POST':
        outputs = []
        output_ids = []
        user_input_sequences = {}
        model = request.POST.get('model', 'GPT3')
        no_of_outputs = int(request.POST.get('no_outputs'))

        for input_sequence in feature.inputs.all():
            user_input = request.POST.get(input_sequence.input_key, None)
            if user_input:
                user_input_sequences[input_sequence.input_key] = input_sequence.prompt.format(user_input=user_input)
            else:
                user_input_sequences[input_sequence.input_key] = ''

        declutter = DeClutter(feature)

        if request.user.tokens > (200 * (no_of_outputs - 1)):
            while no_of_outputs > 0:
                output = declutter.execute(user_input_sequences, model)

                if 'error' in output:
                    return JsonResponse({'error': output['error'], 'status': 500})

                outputs.append(output['result'])
                output_ids.append(save_output(output['result'], model, feature, request.user))
                no_of_outputs -= 1

            return JsonResponse({'outputs': outputs, 'output_ids': output_ids, 'status': 201}, status=http.HTTPStatus.OK)

        else:
            return JsonResponse({'error': 'You are out of words please upgrade your plan to get more words.', 'status': 400})

    page = 'features'

    context = {
        'page': page,
        'feature': feature
    }

    return render(request, 'app.html', context)
