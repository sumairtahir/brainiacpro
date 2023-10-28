from django.contrib import admin

from features.models import OutputHistory, Feature, InputSequence, Option, FavoriteFeature, Category

# Register your models here.
admin.site.register(InputSequence)
admin.site.register(Option)
admin.site.register(Feature)
admin.site.register(OutputHistory)
admin.site.register(FavoriteFeature)
admin.site.register(Category)
