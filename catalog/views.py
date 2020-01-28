from django.shortcuts import render
from django.views.generic import TemplateView # Import TemplateView
from django.http import HttpResponse,  HttpResponseRedirect


class IndexPageView(TemplateView):
    template_name = "index.html"


class AboutUsPageView(TemplateView):
    template_name = "aboutus.html"


class WhatWeDoPageView(TemplateView):
    template_name = "whatwedo.html"


class ProductsPageView(TemplateView):
    template_name = "products.html"

def HomeRedirect(request):
    return HttpResponseRedirect("/index")

def ERR404(request):
    return HttpResponse("404")