from django.views.generic import TemplateView
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
    template_name = 'node.html'
    print(node)
    return HttpResponse(node)
    