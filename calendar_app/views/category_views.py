
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from ..forms import CategoryForm
from ..models import Category


class CategoryListView(generic.ListView):
    model = Category

def createCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            task = form.save()
            return redirect('index')
    else:
        form = CategoryForm()

    context = {'form': form}
    return render(request, 'calendar_app/create_category_form.html', context)

def updateCategory(request,category_id):
    category = get_object_or_404(Category,pk=category_id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
         form = CategoryForm(request.POST, instance=category)
         if form.is_valid():
             form.save()
         return redirect('category-list')

    context = {'form': form,'category':category}
    return render(request, 'calendar_app/update_category_form.html', context)

def deleteCategory(request,category_id):
    category = get_object_or_404(Category,pk=category_id)
    if request.method == 'POST':
       category.delete()
       return redirect('index')
    context = {'category':category}
    return render(request, 'calendar_app/delete_category_form.html', context)