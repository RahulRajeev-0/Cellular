from django.shortcuts import render,redirect
from categoryManagement.models import Category
from categoryManagement.forms import CategoryForm
from django.shortcuts import get_object_or_404
# Create your views here.
def add_category(request):
    if 'email' not in request.session:
        return redirect ('admin_panel:admin_login')
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category:add_category")
    else:
        form = CategoryForm
    list = Category.objects.all()
    return render(request, 'category/adding_cat.html', {'form':form , 'list':list})
    
def edit_cat(request,cat_id):
    category = get_object_or_404(Category , id = cat_id)
    if request.method == "POST":
        form = CategoryForm(request.POST , instance = category)
        if form.is_valid():
            form.save()
            return redirect('category:add_category')
    else:
        form = CategoryForm(instance = category)
    return render (request, 'category/edit_cat.html',{'form':form})
