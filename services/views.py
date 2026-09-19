from django.shortcuts import render, get_object_or_404
from .models import ServiceCategory


def category_list(request):
    categories = ServiceCategory.objects.all()
    return render(request, 'services/category_list.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    return render(request, 'services/category_detail.html', {'category': category})