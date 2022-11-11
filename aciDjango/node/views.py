from django.views.generic import TemplateView
from django.shortcuts import render
from .services import get_droplets,login_aci,getnodes
from django.http import HttpResponse

class GetNode(TemplateView):
    template_name = 'node.html'
    
    def get_context_data(self, *args, **kwargs):
        login_aci()
        context = {
            'nodes' : getnodes(),
        }

        return context

def GetNodeInfo(request, node):
    print(node)
    return HttpResponse(node)
    