from django.shortcuts import render
from django.views.generic import TemplateView # Import TemplateView
from django.http import HttpResponse,  HttpResponseRedirect

import json

class AboutUsPageView(TemplateView):
    template_name = "aboutus.html"


class WhatWeDoPageView(TemplateView):
    template_name = "whatwedo.html"


class ProductsPageView(TemplateView):
    template_name = "products.html"

def HomeRedirect(request):
    return HttpResponseRedirect("/")

def index_view(request):
    context = {"urls" : {
                    "blog" : "/blog",
                    "aboutus": "/aboutus",
                    "products" : "/products",
                    "pricing" : "/subscriptions/plans",
                }}
    # if "REDIRECT_URL" in request.sessions:
    URL = request.session.get("REDIRECT_URL")
    if 'REDIRECT_URL' in request.session: del request.session['REDIRECT_URL']
    if URL : 
       return HttpResponseRedirect(URL)
    return render(request, "index.html", context=context)


def ERR404(request, slug):
    return render(request,"404page.html")


def update_session(request):
    data = json.loads(request.GET.get("data"))
    request.session['data'] = data
    return HttpResponse(f'{data} : {request.GET}')