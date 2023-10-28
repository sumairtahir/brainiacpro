from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from authentication.decorators import subscription_required
from automation.models import Automation, Operation, OperationOutputKeys
from .tasks import create_default_output_keys, get_prev_operation_outputs_keys, start_automation


@login_required(login_url='login')
@subscription_required()
def automation_view(request):
    '''
    Automation.
    '''
    automation = Automation.objects.get(id=1)
    operations = Operation.objects.filter(automation_id=1)
    
    if request.method == 'POST':
        print("HERE")
        start_automation(1)
        # operation = Operation.objects.filter(automation_id=1, prev_operation=None).first()
        # last_operation = get_last_operation(operation)
        # call_operation(operation, 1, True, 1, last_operation)
    print("here 2")
    page = 'automation'

    context = {
        'automation': automation,
        'page': page,
        'operations': operations
    }

    return render(request, 'automation.html', context)


@login_required(login_url='login')
@subscription_required()
def get_operation_settings(request, operation_id):
    '''
    get_operation_settings.
    '''

    operation = Operation.objects.filter(id=operation_id).first()
    operations = Operation.objects.filter(id=operation_id).values().first()
    expected_outputs = {key: value for key, value in Operation.output_type}
    operation_output_keys = OperationOutputKeys.objects.filter(operation_id=operation.id)

    if not operation_output_keys:
        create_default_output_keys(operation)

    previous_outputs = []
    if operation.prev_operation:
        previous_outputs = list(get_prev_operation_outputs_keys(operation.prev_operation).values())

    context = {
        'operations': operations,
        'expected_outputs': expected_outputs,
        'previous_outputs': previous_outputs,
    }

    return JsonResponse(context)


def edit_operation_settings(request, operation_id):

    operation = Operation.objects.filter(id=operation_id).first()
    if operation:
        text_field_1 = request.POST.get("text_field_1", operation.text_field_1)
        text_field_2 = request.POST.get("text_field_2", operation.text_field_1)
        text_area_1 = request.POST.get("text_area_1", operation.text_area_1)
        expected_output = request.POST["expected_output"]
        
        if "file" in request.FILES:
            operation.file = request.FILES["file"]

        operation.text_area_1 = text_area_1
        operation.text_field_1 = text_field_1
        operation.text_field_2 = text_field_2
        operation.expected_output = expected_output
        operation.save()

    return JsonResponse({})


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def test_channels(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'operations_group',
        {
            'type': 'update_status',
            'operation_name': "Test Operation",
            'status': 'completed'
        }
    )
