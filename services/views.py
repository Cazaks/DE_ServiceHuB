from django.shortcuts import render
from .models import ServiceCategory


def category_list(request):
    categories = ServiceCategory.objects.all()
    return render(request, 'services/category_list.html', {'categories': categories})
