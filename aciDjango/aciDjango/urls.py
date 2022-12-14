"""aciDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from node.views import GetNode, GetNodeInfo
from findsfp.views import GetSFP
from dci.views import GetStatusVLAN, GetStatusVXLAN, GetStatusDCI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GetNode.as_view(template_name='node.html'), name='Node View'),
    path('node/<int:node>/', GetNodeInfo),
    path('findsfp/', GetSFP.as_view(template_name='sfp.html'), name='Find SFP'),
    path('dci/<int:vlan>/', GetStatusVLAN, name='Check DCI'),
    path('dci/', GetStatusDCI, name='Check DCI'),
]

# from django.views.generic import RedirectView
# urlpatterns += [
#     path('', RedirectView.as_view(url='/catalog/', permanent=True)),
# ]


# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)