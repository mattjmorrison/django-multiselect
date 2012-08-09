
from django import forms
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
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

    def render(self, name, value, attrs=None, choices=()):
        attrs = attrs or {}
        attrs['class'] = 'selectfilter'
        if self.is_stacked:
            attrs['class'] += 'stacked'

        attrs['data-verbose-name'] = self.verbose_name.replace('"', '\\"')
        attrs['data-is-stacked'] = int(self.is_stacked)
        attrs['data-static'] = static('multiselect/')

        output = [super(FilteredSelectMultiple, self).render(name, value, attrs, choices)]
        return mark_safe(u''.join(output))

    class Media(object):
        _media = "multiselect/{typ}/DjangoSelect.{typ}"
        js = [static(_media.format(typ='js'))]
        css = {'all': [static(_media.format(typ='css'))]}
