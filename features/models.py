from django.db import models
from django.utils import timezone

from authentication.models import Account

# Create your models here.
class InputSequence(models.Model):
    input_type_choices = (
        ("text_field", "Input Text Field"),
        ("textarea", "TextArea"),
        ("select_picker", "Select Picker"),
    )
    title = models.CharField(max_length=256)
    input_key = models.CharField(max_length=256)
    placeholder = models.CharField(max_length=256)
    input_type = models.CharField(max_length=64, choices=input_type_choices)
    input_length = models.IntegerField(default=80)
    is_required = models.IntegerField(default=0)
    prompt = models.TextField(default='{user_input}')

    def __str__(self) -> str:
        return self.input_key + ": "+ self.prompt


class Option(models.Model):
    input_sequence = models.ForeignKey(InputSequence, on_delete=models.CASCADE, related_name="options")
    title = models.CharField(max_length=256)
    option_key = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.title
    

class Category(models.Model):
    title = models.CharField(max_length=126, default="")
    code = models.CharField(max_length=126, default="")


class Feature(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=512)
    prompt = models.TextField()
    description = models.TextField()
    meta_description = models.CharField(max_length=256)
    icon = models.ImageField(blank=True, upload_to='features/icons')
    inputs = models.ManyToManyField(InputSequence, default=None, null=True)
    category = models.ManyToManyField(Category, null=True, blank=True)


    def __str__(self) -> str:
        return self.title
    

class FavoriteFeature(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="favorite_features")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    is_fav = models.IntegerField(default=0)


class Recipes(models.Model):
    title = models.CharField(max_length=256)
    recipe = models.TextField()
    feature = models.ForeignKey(Feature, related_name="recipes", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class OutputHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    model = models.CharField(max_length=128, default="gpt-J")
    input_sequence = models.TextField(default="")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="output", default=None, null=True)
    tokens = models.IntegerField(default=0)
    output = models.TextField(default="")
    stared = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


class DocumentHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    document_text = models.TextField()
    timpstamp = models.DateField(default=timezone.now)
    model = models.CharField(max_length=128, default="gpt-J")
    task = models.CharField(max_length=300, default="Text Simplification")
    stared = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)