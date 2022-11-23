from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from .nxos_api import n9k_vlans, n7k_vlans
from django.template.loader import get_template

devicesChecked = []
devices_list = []

devices_list.append({
        'device':"10.227.70.145",
        'device_type': "n9k",
        'username': "admin",
        'password': "admin"
    })


class GetStatusVXLAN(TemplateView):
    template_name = 'sfp.html'
    def get_context_data(self, *args, **kwargs):
        context = {
            'listsfp': captureHost()
        }
        return context

def GetStatusVLAN(request, vlan):
    for device in devices_list:
        if device["device_type"] == "n9k":
            # [   
            #     0: {
            #         "device": device,
            #         "Po20": True
            #         "Po17": "cli_show",
            #         "SPT": True,
            #         "sid": "1",
            #         "input": "show vlan id "+vlan+" ;show spanning-tree vlan "+vlan+"",
            #         "output_format": "json"
            #     }
            #     1: {...}
            # ]

            # def n7k_vlans(device,vlan,username,password):
            devicesChecked.append(n9k_vlans(device["device"],vlan,device["username"],device["password"]))
        if device["device_type"] == "n7k":
            devicesChecked.append(n7k_vlans(device["device"],vlan,device["username"],device["password"]))
    context = {
        'devicesChecked': devicesChecked,
        'vlan': vlan
    }
    print (context)
    return render(request, 'vlan.html', context)


# [   
#     0: {
#         "device": device,
#         "Po20": True
#         "Po17": "cli_show",
#         "SPT": True,
#         "sid": "1",
#         "input": "show vlan id "+vlan+" ;show spanning-tree vlan "+vlan+"",
#         "output_format": "json"
#     }
#     1: {...}
# ]


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))