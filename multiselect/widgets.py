
from django import forms
from django.conf import settings

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
