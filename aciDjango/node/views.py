from django.views.generic import TemplateView
from .services import get_droplets,login_aci,getnodes

class GetNode(TemplateView):
    template_name = 'node.html'
    
    def get_context_data(self, *args, **kwargs):
        login_aci()
        print (getnodes())
        context = {
            'nodes' : getnodes(),
        }

        return context
    