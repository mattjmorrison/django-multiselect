import re
from django import test

from multiselect import models
from multiselect import widgets, forms, fields

class MultiSelectWidgetTests(test.TestCase):

    def should_set_attrs_class_when_no_attrs_present(self):
        widget = widgets.MultiSelectWidget()
        self.assertEqual('multiselect', widget.attrs['class'])

    def should_add_class_to_attrs_when_attrs_present(self):
        widget = widgets.MultiSelectWidget(attrs={'border':'1'})
        self.assertEqual({'class':'multiselect', 'border':'1',},
                          widget.attrs)

    def should_add_additional_class_when_class_is_already_specified(self):
        widget = widgets.MultiSelectWidget(attrs={'class':'klass'})
        self.assertEqual({'class':'klass multiselect'},widget.attrs)

    def should_include_ui_multiselect_js_in_widget_media(self):
        self.assertRegExInList("ui\.multiselect\.js$", widgets.MultiSelectWidget.Media.js,
                               "widget didn't contain ui.multiselect.js in js media")

    def should_include_multiselect_css_in_widget_media(self):
        self.assertRegExInList("ui\.multiselect\.css$", widgets.MultiSelectWidget.Media.css['all'],
                               "widget didn't contain ui.multiselect.css in css media")

    def assertRegExInList(self, regex, string_list, msg='Regex not found'):
        for item in string_list:
            if re.search(regex, item):
                break
        else:
            self.fail(msg)

class MultipleChoiceFieldTests(test.TestCase):

    def should_use_multiselect_widget(self):
        form = forms.SelectForm()
        self.assertTrue(isinstance(form.fields['choices'].widget, widgets.MultiSelectWidget))

class ModelMultipleChoiceFieldTests(test.TestCase):

    def should_use_multiselect_widget(self):
        form = forms.ModelSelectForm()
        self.assertTrue(isinstance(form.fields['choices'].widget, widgets.MultiSelectWidget))

class ManyToManyFieldTests(test.TestCase):

    def should_not_include_any_default_help_text(self):
        self.assertEqual('', unicode(fields.ManyToManyField(models.SampleModel).help_text))

    def should_use_help_text_declared_in_model_when_present(self):
        field = fields.ManyToManyField(models.SampleModel, help_text="help me")
        self.assertEqual("help me", field.help_text)
