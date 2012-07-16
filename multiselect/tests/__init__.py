import re
from django import test
from django.db.models import Model, CharField, TextField
from django.forms import Form, ModelForm
from multiselect import widgets, fields


class Choice(Model):
    choice = CharField(max_length=15)

    def __unicode__(self):
        return self.choice


class SampleModel(Model):
    name = CharField(max_length=15)
    choices = fields.ManyToManyField(Choice)
    passwd = TextField()

    def verbose_label(self):
        return unicode(self.name)

    def __unicode__(self):
        return unicode(self.pk)


class SelectForm(Form):
    CHOICES = (('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'))
    choices = fields.MultipleChoiceField(choices=CHOICES)


class ModelSelectForm(ModelForm):

    class Meta:
        model = SampleModel


class MultiSelectWidgetTests(test.TestCase):

    def test_set_attrs_class_when_no_attrs_present(self):
        widget = widgets.MultiSelectWidget()
        self.assertEqual('multiselect', widget.attrs['class'])

    def test_add_class_to_attrs_when_attrs_present(self):
        widget = widgets.MultiSelectWidget(attrs={'border':'1'})
        self.assertEqual({'class':'multiselect', 'border':'1',},
            widget.attrs)

    def test_add_additional_class_when_class_is_already_specified(self):
        widget = widgets.MultiSelectWidget(attrs={'class':'klass'})
        self.assertEqual({'class':'klass multiselect'},widget.attrs)

    def test_include_ui_multiselect_js_in_widget_media(self):
        self.assertRegExInList("ui\.multiselect\.js$", widgets.MultiSelectWidget.Media.js,
            "widget didn't contain ui.multiselect.js in js media")

    def test_include_multiselect_css_in_widget_media(self):
        self.assertRegExInList("ui\.multiselect\.css$", widgets.MultiSelectWidget.Media.css['all'],
            "widget didn't contain ui.multiselect.css in css media")

    def assertRegExInList(self, regex, string_list, msg='Regex not found'):
        for item in string_list:
            if re.search(regex, item):
                break
        else:
            self.fail(msg)


class MultipleChoiceFieldTests(test.TestCase):

    def test_use_multiselect_widget(self):
        form = SelectForm()
        self.assertTrue(isinstance(form.fields['choices'].widget, widgets.MultiSelectWidget))


class ModelMultipleChoiceFieldTests(test.TestCase):

    def test_use_multiselect_widget(self):
        form = ModelSelectForm()
        self.assertTrue(isinstance(form.fields['choices'].widget, widgets.MultiSelectWidget))

    def test_uses_verbose_label_when_obj_has_attribute(self):
        model = SampleModel(name="A name")
        f = fields.ModelMultipleChoiceField(SampleModel.objects.all())
        self.assertEqual(model.verbose_label(), f.label_from_instance(model))

    def test_uses_super_label_from_instance_when_object_doesnt_have_verbose_label(self):
        model = Choice(choice='a choice')
        f = fields.ModelMultipleChoiceField(Choice.objects.all())
        self.assertEqual(str(model), f.label_from_instance(model))


class ManyToManyFieldTests(test.TestCase):

    def test_not_include_any_default_help_text(self):
        self.assertEqual('', unicode(fields.ManyToManyField(SampleModel).help_text))

    def test_use_help_text_declared_in_model_when_present(self):
        field = fields.ManyToManyField(SampleModel, help_text="help me")
        self.assertEqual("help me", field.help_text)
