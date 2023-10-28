from django.contrib import admin

# Register your models here.
from .models import Automation, Operation, OperationOutputKeys
# Register your models here.

admin.site.register(Automation)
admin.site.register(Operation)
admin.site.register(OperationOutputKeys)
