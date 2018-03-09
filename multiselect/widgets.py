from itertools import chain
from django import forms
from django.conf import settings
from django.utils.encoding import force_text
from django.forms.utils import flatatt
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class MultiSelectWidget(forms.SelectMultiple):
    css_class = 'multiselect'

    class Media(object):
        css = {
            'all': (
                settings.STATIC_URL + 'multiselect/css/ui.multiselect.css',
                settings.STATIC_URL + 'multiselect/css/themes/smoothness/jquery-ui-1.7.1.custom.css',
            )
        }
        js = (
            settings.STATIC_URL + 'multiselect/js/ui.multiselect.js',
        )

    def add_css_class(self, attrs):
        attrs = attrs or {}
        if 'class' in attrs:
            attrs['class'] += " %s" % self.css_class
        else:
            attrs['class'] = self.css_class
        return attrs

    def __init__(self, attrs=None):
        attrs = self.add_css_class(attrs)
        super(MultiSelectWidget, self).__init__(attrs=attrs)


class FilteredSelectMultiple(forms.SelectMultiple):

    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        self.verbose_name = verbose_name
        self.is_stacked = is_stacked
        super(FilteredSelectMultiple, self).__init__(attrs, choices)

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{}"{}>{}</option>',
                           option_value,
                           selected_html,
                           force_text(option_label))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

    def old_render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, {'name': name})
        output = [format_html('<select multiple="multiple"{}>', flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))

    def render(self, name, value, attrs=None, choices=()):
        attrs = attrs or {}
        attrs['class'] = 'selectfilter'
        if self.is_stacked:
            attrs['class'] += 'stacked'

        attrs['data-verbose-name'] = self.verbose_name.replace('"', '\\"')
        attrs['data-is-stacked'] = int(self.is_stacked)
        attrs['data-static'] = static('multiselect/')

        output = [self.old_render(name, value, attrs, choices)]
        return mark_safe(u''.join(output))

    class Media(object):
        _media = "multiselect/{typ}/DjangoSelect.{typ}"
        js = [static(_media.format(typ='js'))]
        css = {'all': [static(_media.format(typ='css'))]}
