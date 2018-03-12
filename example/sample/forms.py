
from django import forms
from multiselect.fields import MultipleChoiceField
from example.sample import models
from multiselect.widgets import FilteredSelectMultiple


class SelectForm(forms.Form):
    CHOICES = (('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'))
    choices = MultipleChoiceField(choices=CHOICES)


class ModelSelectForm(forms.ModelForm):

    class Meta:
        model = models.SampleModel
        fields = ['name', 'choices', 'passwd']


class SelectForm2(forms.Form):
    CHOICES = (('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'))
    choices = MultipleChoiceField(choices=CHOICES, widget=FilteredSelectMultiple('Choices', is_stacked=False))


class ModelSelectForm2(forms.ModelForm):

    class Meta:
        model = models.SampleModel
        widgets = {'choices': FilteredSelectMultiple('Choices', is_stacked=False)}
        fields = ['name', 'choices', 'passwd']
