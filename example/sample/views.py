# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response

from example.sample import forms

def index(request):
    data = {'form': forms.SelectForm(), 'modelform':forms.ModelSelectForm()}
    
    return render_to_response("multiselect/index.html", data,
                              context_instance=RequestContext(request))

def index2(request):
    data = {'form': forms.SelectForm2(), 'modelform':forms.ModelSelectForm2()}

    return render_to_response("multiselect/index.html", data,
                              context_instance=RequestContext(request))
