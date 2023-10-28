import re
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import pandas as pd
from .models import Operation, OperationOutputKeys
from celery import shared_task
from .apis.wordpress import WordPress


wordpress = WordPress('sumair', 'yEaNclS3vRT19GbJgVbulbjf', 'dreaminterpreter.pro')


def update_status(operation_id, status):
    # Notify clients about the updated status
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'operations_group',
        {
            'type': 'update_status',
            'operation_id': operation_id,
            'status': status,
        }
    )


def update_iterations(operation_id, iteration_count, total_iterations):
    # Notify clients about the updated status
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'operations_group',
        {
            'type': 'update_iterations',
            'operation_id': operation_id,
            'iteration_count': iteration_count,
            'total_iterations': total_iterations
        }
    )


def queryset_to_output_dict(previous_outputs):
    output_dict = {}
    for obj in previous_outputs:
        output_dict[obj.output_key] = obj.output
    return output_dict


def get_last_operation(operation):
    if operation.next_operations.all():
        last_next_operation = operation.next_operations.all().order_by('priority').first()
        operation = get_last_operation(last_next_operation)

    return operation


def cleanup_outputs(automation_id):
    operations = Operation.objects.filter(automation_id=automation_id)
    for operation in operations:
        operation.operation_outputs.all().update(output="")


def set_output(operation, ouput_key, output):
    operation_output_key = OperationOutputKeys.objects.get(operation_id=operation.id, output_key=ouput_key.lower().replace(" ", "_"))
    operation_output_key.output = output
    operation_output_key.save()


def get_prev_operation_outputs_keys(operation):
    operation_output_keys = OperationOutputKeys.objects.filter(operation_id=operation.id)
    previous_operation = operation.prev_operation
    
    if not operation_output_keys:
        operation_output_keys = create_default_output_keys(operation)
        
    if previous_operation:
        previous_output_keys = get_prev_operation_outputs_keys(previous_operation)
        operation_output_keys = operation_output_keys | previous_output_keys
    
    return operation_output_keys


def create_default_output_keys(operation):
    if operation.operation_type == Operation.EXCELFILEUPLOAD:
        excel_file = operation.file
        if not excel_file:
            return

        data_frame = pd.read_csv(excel_file)
        # We are expecting output as the LISTOFROWS
        operation_output_keys = list(data_frame.columns)
    else:
        operation_output_keys = operation.title
        operation_output_title = operation_output_keys + " output"

    if isinstance(operation_output_keys, list):
        for operation_output_key in operation_output_keys:
            operation_output_key = operation_output_key
            operation_output_key = OperationOutputKeys(
                title=operation_output_key,
                output_key=operation_output_key.lower().replace(" ", "_"),
                operation=operation
            )
            operation_output_key.save()

    else:
        operation_output_key = OperationOutputKeys(
            title=operation_output_title,
            output_key=operation_output_keys.lower().replace(" ", "_"),
            operation=operation
        )
        operation_output_key.save()


def call_next_operation(operation_output, operation):

    iteration = 1
    call_next_operation_bool = True
    next_operation = operation.next_operations.all().first()
    
    if next_operation:
        if isinstance(operation_output, list):

            for output in operation_output:
                if isinstance(output, dict):
                    for key, value in output.items():
                        set_output(operation, key, value)
                else:
                    call_next_operation_bool = False
                    set_output(operation, operation.title, output)
                print(iteration, len(operation_output))
                call_operation(next_operation, iteration, call_next_operation_bool, len(operation_output))
                iteration += 1
            
        else:
            set_output(operation, operation.title, operation_output)
            call_operation(next_operation, iteration, call_next_operation_bool, 1)
            

def call_multi_next_operation(operation_output, operation, last_operation):

    call_next_operation_bool = True
    next_operations = operation.next_operations.all().order_by('-priority')
    for next_operation in next_operations:
        iteration = 1
        if isinstance(operation_output, list):

            for output in operation_output:
                if len(operation_output) > 1:
                    update_iterations(next_operation.id, iteration, len(operation_output))
                if isinstance(output, dict):
                    for key, value in output.items():
                        set_output(operation, key, value)
                else:
                    call_next_operation_bool = False
                    set_output(operation, operation.title, output)
                call_operation(next_operation, iteration, call_next_operation_bool, len(operation_output), last_operation)
                iteration += 1
            
        else:
            set_output(operation, operation.title, operation_output)
            call_operation(next_operation, iteration, call_next_operation_bool, 1, last_operation)

import time

def call_operation(operation, iteration, call_next_operation_bool, total_iterations, last_operation):
    
    update_status(operation.id, 2)
    time.sleep(5)
    previous_output_dict = {}
    if operation.prev_operation:
        previous_outputs = get_prev_operation_outputs_keys(operation)
        previous_output_dict = queryset_to_output_dict(previous_outputs)

    if operation.operation_type == Operation.EXCELFILEUPLOAD:
        excel_file = operation.file
        data_frame = pd.read_csv(excel_file)

        if operation.expected_output == operation.LISTOFROWS:
            operation_output = data_frame.to_dict(orient='records')
            # operation_output = data_frame.columns

    if operation.operation_type == Operation.CHATGPT:
        input_sequence = operation.text_area_1
        operation_output_key = OperationOutputKeys.objects.filter(operation_id=operation.id).first()

        gpt3_output = "Content for " + input_sequence
        if operation.expected_output == operation.LISTOFTEXT:
            """Genrate response in a list formate."""
            input_sequence += '\n provide the elements in a python list format use \n for line breaks in the elements. ["heading /nbreif description",...]'
            gpt3_output = 'Sure here is it ["Heading 1", "Heading 2", "heading 3"]'

        # gpt3 = GPT3("", input_sequence, previous_output_dict)
        # gpt3_output = gpt3.generate(mode=GPT.TEXT)

        if operation.expected_output == operation.LISTOFTEXT:
            """Extract list from chat gpt response here"""

            pattern = r'\[([^\[\]]*)\]'
            match = re.search(pattern, gpt3_output)
            list_str = match.group(1)
            operation_output = [item.strip() for item in list_str.split(",")]
        else:
            # output_list = ast.literal_eval(operation_output_key.output)
            # if not isinstance(output_list, list):
            #     output_list = []

            operation_output_key.output += "\n" + gpt3_output.format(**previous_output_dict)
            operation_output = str(operation_output_key.output)
            operation_output_key.save()

    if operation.operation_type == Operation.DALLE:
        # gpt3 = GPT3("", input_sequence, previous_output_dict)
        # operation_output = gpt3.generate(mode=GPT.IMAGE)
        operation_output = "some_image_url"

    if operation.operation_type == Operation.WORDPRESSPOSTARTICLE:
        title = operation.text_field_1.format(**previous_output_dict)
        content = operation.text_area_1.format(**previous_output_dict)
        operation_output = ""  # wordpress.add_draft_post(title, content)

    if operation == last_operation:
        cleanup_outputs(1)
    
    if iteration == total_iterations:
        update_status(operation.id, 3)
        
    if call_next_operation_bool:
        call_multi_next_operation(operation_output, operation, last_operation)
    else:
        if iteration == total_iterations:
            call_multi_next_operation(operation_output, operation, last_operation)
        else:
            set_output(operation, operation.title, operation_output)



@shared_task
def start_automation(automation_id):
    # Perform the background operation
    # ...
    operation = Operation.objects.filter(automation_id=automation_id, prev_operation=None).first()
    last_operation = get_last_operation(operation)
    call_operation(operation, 1, True, 1, last_operation)

    # # Update the operation status to "completed"
    # operation = Operation.objects.get(id=1)
    # operation.status = 1
    # operation.save()

    # update_status(1, 2)
    # update_iterations(1, 2, 1000)
