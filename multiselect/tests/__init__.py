from textwrap import dedent
import re
from django import test
from django.db.models import Model, CharField, TextField
from django.forms import Form, ModelForm
from multiselect import widgets, fields


class Choice(Model):
    choice = CharField(max_length=15)

    def __str__(self):
        return self.choice


class SampleModel(Model):
    name = CharField(max_length=15)
    choices = fields.ManyToManyField(Choice)
    passwd = TextField()

    def verbose_label(self):
        return self.name

    def __str__(self):
        return self.pk


class SelectForm(Form):
    CHOICES = (('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'))
    choices = fields.MultipleChoiceField(choices=CHOICES)


class ModelSelectForm(ModelForm):

    class Meta:
        model = SampleModel
        fields = ['name', 'choices', 'passwd']


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
        self.assertEqual('', fields.ManyToManyField(SampleModel).help_text)

    def test_use_help_text_declared_in_model_when_present(self):
        field = fields.ManyToManyField(SampleModel, help_text="help me")
        self.assertEqual("help me", field.help_text)


class FilteredSelectMultiple(test.TestCase):

    def test_sets_verbose_name_in_init(self):
        widget = widgets.FilteredSelectMultiple('This is my name', is_stacked=False)
        self.assertEqual("This is my name", widget.verbose_name)

    def test_sets_is_stacked_in_init(self):
        widget = widgets.FilteredSelectMultiple('This is my name', is_stacked=False)
        self.assertFalse(widget.is_stacked)

    def test_renders_select(self):
        choices = ((0, 'A'), (1, 'B'), (2, 'C'))
        widget = widgets.FilteredSelectMultiple('This is my name', is_stacked=False, choices=choices)
        data_attrs = 'data-verbose-name="This is my name" data-static="/static/multiselect/"'
        self.assertCountEqual(dedent("""
        <select multiple="multiple" {} name="Name" data-is-stacked="0" class="selectfilter">
        <option value="0">A</option>
        <option value="1" selected="selected">B</option>
        <option value="2" selected="selected">C</option>
        </select>
        """).strip().format(data_attrs), widget.render("Name", (1, 2)))

    def test_sets_is_stacked_data_attribute_when_false(self):
        widget = widgets.FilteredSelectMultiple('', is_stacked=False)
        self.assertIn('data-is-stacked="0"', widget.render('', ''))

    def test_sets_stacked_class_when_is_stacked(self):
        widget = widgets.FilteredSelectMultiple('', is_stacked=True)
        self.assertRegexpMatches(widget.render('', ''), 'class="[^"]*stacked[^"]*"')

    def test_does_not_set_stacked_class_when_is_not_stacked(self):
        widget = widgets.FilteredSelectMultiple('', is_stacked=False)
        self.assertRegexpMatches(widget.render('', ''), 'class="(?![^"]*stacked[^"]*).*"')

    def test_sets_is_stacked_data_attribute_when_true(self):
        widget = widgets.FilteredSelectMultiple('', is_stacked=True)
        self.assertIn('data-is-stacked="1"', widget.render('', ''))

    def test_sets_verbose_name_data_attribute(self):
        widget = widgets.FilteredSelectMultiple('XXXXX', is_stacked=True)
        self.assertIn('data-verbose-name="XXXXX"', widget.render('', ''))

    def test_sets_static_data_attribute(self):
        widget = widgets.FilteredSelectMultiple('', is_stacked=True)
        self.assertIn('data-static="/static/multiselect/"', widget.render('', ''))

    def test_includes_js_in_widget_media(self):
        self.assertEqual(
            ["/static/multiselect/js/DjangoSelect.js"],
            widgets.FilteredSelectMultiple.Media.js
        )

    def test_includes_css_in_widget_media(self):
        self.assertEqual(
            ["/static/multiselect/css/DjangoSelect.css"],
            widgets.FilteredSelectMultiple.Media.css['all']
        )
