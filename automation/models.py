from django.db import models
from authentication.models import Account
# Create your models here.


class Automation(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)


class Operation(models.Model):
    LISTOFTEXT = 1
    TEXT = 2
    LISTOFROWS = 3
    ROW = 4
    output_type = (
        (LISTOFTEXT, "List of Text"),
        (TEXT, "Text"),
        (LISTOFROWS, "List of Rows"),
        (ROW, "Single Row")
    )

    EXCELFILEUPLOAD = 1
    CHATGPT = 2
    DALLE = 3
    WORDPRESSPOSTARTICLE = 4

    automation = models.ForeignKey(Automation, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    operation_title = models.CharField(max_length=256)
    operation_type = models.IntegerField(default=1)
    file = models.FileField(upload_to="automation/operations/files", null=True, blank=True)
    text_field_1 = models.CharField(max_length=512, blank=True, null=True)
    text_field_2 = models.CharField(max_length=512, blank=True, null=True)
    text_area_1 = models.TextField(blank=True, null=True)
    expected_output = models.IntegerField(blank=True, null=True, choices=output_type)
    # call_same_operation = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    iteration = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    prev_operation = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="next_operations")
    icon = models.ImageField(blank=True, upload_to='automation/icons')

    def __str__(self) -> str:
        return self.title


class OperationOutputKeys(models.Model):
    title = models.CharField(max_length=256)
    output_key = models.CharField(max_length=256)
    output = models.TextField(blank=True)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name="operation_outputs")

    def __str__(self) -> str:
        return self.output_key + ": " + self.title
