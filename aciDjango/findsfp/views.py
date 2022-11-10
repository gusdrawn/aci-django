from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.
def GetSFP(requests):
    
    return HttpResponse("Welcome to Find SFP page")


class GetSFP(TemplateView):
    template_name = 'sfp.html'
    def get_context_data(self, *args, **kwargs):
        context = {
            'nodes' : 'test',
        }
        return context