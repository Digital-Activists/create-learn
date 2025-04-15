from django.shortcuts import render


def index(request):
    template_name = "includes/index.html"
    return render(request, template_name)
