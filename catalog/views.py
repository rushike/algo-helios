from django.shortcuts import render
from django.views.generic import TemplateView # Import TemplateView

# Create your views here.


# Add the two views we have been talking about  all this time :)
class IndexPageView(TemplateView):
    template_name = "index.html"


class AboutUsPageView(TemplateView):
    template_name = "aboutus.html"


class WhatWeDoPageView(TemplateView):
    template_name = "whatwedo.html"


class ProductsPageView(TemplateView):
    template_name = "products.html"
