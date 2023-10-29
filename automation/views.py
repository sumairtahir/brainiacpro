from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from authentication.decorators import subscription_required
from automation.models import Automation, Operation, OperationOutputKeys
from .tasks import create_default_output_keys, get_prev_operation_outputs_keys, start_automation


def get_next_operations(operation, operations):
    next_operations = operation.next_operations.all().order_by('-priority')
    if next_operations:
        for next_operation in next_operations:
            operations.append(next_operation)
            operations = get_next_operations(next_operation, operations)

    return operations
        

@login_required(login_url='login')
@subscription_required()
def automation_view(request):
    '''
    Automation.
    '''
    automation = Automation.objects.get(id=1)
    operations_list = []
    operations = Operation.objects.filter(automation_id=1, prev_operation=None).order_by('-priority')
    for operation in operations:
        operations_list.append(operation)
        operations_list = get_next_operations(operation, operations_list)
    
    if request.method == 'POST':
        start_automation.delay(1)

    page = 'automation'

    context = {
        'automation': automation,
        'page': page,
        'operations': operations_list
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
        text_field_2 = request.POST.get("text_field_2", operation.text_field_2)
        image_url = request.POST.get("image_url", operation.image_url)
        text_area_1 = request.POST.get("text_area_1", operation.text_area_1)
        expected_output = request.POST["expected_output"]
        
        if "file" in request.FILES:
            operation.file = request.FILES["file"]

        operation.text_area_1 = text_area_1
        operation.text_field_1 = text_field_1
        operation.text_field_2 = text_field_2
        operation.image_url = image_url
        operation.expected_output = expected_output
        operation.save()

    return JsonResponse({})
