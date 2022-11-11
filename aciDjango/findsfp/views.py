from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from .host_type import aciHost


# Create your views here.

def captureHost():
    ##if type == 'aci':
        ## def aciHost(ip,username, password,site,context):
        ##aciHost()
    devlist = aciHost('https://10.0.0.1','UserA','SuperSecret','SiteA')
    return devlist

class GetSFP(TemplateView):
    template_name = 'sfp.html'
    def get_context_data(self, *args, **kwargs):
        context = {
            'listsfp': captureHost()
        }
        return context