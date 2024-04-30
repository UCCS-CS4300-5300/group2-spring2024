
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from guardian.decorators import permission_required_or_403

from ..forms import CategoryForm
from ..models import Category, CustomUser


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryListView(generic.ListView):
    model = Category

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('name')


@login_required(login_url='/login/')
def createCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            # Save the form data to the database
            form.save()
        return redirect('category-list')
    else:
        form = CategoryForm()

    context = {'form': form, 'title': 'Create a New Category'}
    return render(request, 'calendar_app/create_category_form.html', context)


@login_required(login_url='/login/')
@permission_required_or_403('change_category', (Category, 'pk', 'category_id'))
def updateCategory(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
        return redirect('category-list')

    context = {'form': form, 'category': category, 'title': 'Update Category'}
    return render(request, 'calendar_app/update_category_form.html', context)


@login_required(login_url='/login/')
@permission_required_or_403('delete_category', (Category, 'pk', 'category_id'))
def deleteCategory(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('index')
    context = {'category': category}
    return render(request, 'calendar_app/delete_category_form.html', context)
