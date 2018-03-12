This project provides a multiselect widget for Django.
============================================================

We're using https://github.com/michael/multiselect for the widget itself and we started with 
http://djangosnippets.org/snippets/2079/ but added a few more things including:

- Integration with Django's admin site
- A model field that will use the multiselect widget by default
- A form field that will use the multiselect widget by default


HOW TO USE AS A FIELD:
============================================================
- In Your Models:
	Use multiselect.fields.ManyToManyField instead of django.db.models.ManyToManyField

- In Your Forms:
	Use multiselect.fields.MultipleChoiceField instead of django.forms.MultipleChoiceField

- If you want to just use the widget:
	set widget=multiselect.widgets.MultiSelect() on your form's field

DEPENDENCIES:
============================================================
The following will need to be manually added to your template(s) so they are available to the widget

- A jquery theme (like this one):
	multiselect/static/css/themes/smoothness/jquery-ui-1.7.1.custom.css

- JQuery 
	https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js

- JQueryUI
	https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js

USING THE MULTISELECT WIDGET IN DJANGO'S ADMIN SITE:
============================================================

The admin site needs the same dependencies, here is how we added them.  We created our own admin/base_site.html
(make sure it is in your template_dirs in settings.py) You can either copy Django's admin/base_site.html as a starting point, our use ours.

Just add the following::

    {% block extrahead %}
        <link type="text/css" rel="stylesheet" href="{% static 'css/themes/smoothness/jquery-ui-1.7.1.custom.css' %}" />
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js"></script>

        <style type="text/css">
            form .ui-multiselect {margin-right: 5px; float: left; border-color: #ccc;}
            form .ui-multiselect div.selected {border-color: #ccc;}
        </style>
    {% endblock %}

This will add jquery, jquery-ui, a jquery-ui theme and some css so the multiselect widget will play nicely with
the Django admin site's styles

Note: We disabled some of the options like draggable and sortable because
they didn't seem to work well and I didn't like the animations anyways.

