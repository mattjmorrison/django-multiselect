from django.contrib import admin
from example.sample.models import SampleModel, Choice

admin.site.register(Choice)
admin.site.register(SampleModel)