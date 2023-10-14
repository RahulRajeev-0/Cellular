from django.urls import path
from categoryManagement import views

app_name = 'category'

urlpatterns = [
    path('add_category/', views.add_category , name = 'add_category'),
    path('edit_cat/<int:cat_id>/' , views.edit_cat , name = 'edit_cat'),
]
