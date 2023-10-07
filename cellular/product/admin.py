from django.contrib import admin
from .models import *




# registering models 




class ProductImageAdmin(admin.StackedInline):
    model =ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name']
    

@admin.register(ColorVarient)
class ColorVarientAdmin(admin.ModelAdmin):
    list_display=['color_name']
    model= ColorVarient

@admin.register(RamVarient)
class RamVarientAdmin(admin.ModelAdmin):
    list_display=['ram_no']
    model= RamVarient

admin.site.register(Brand)
admin.site.register(Product , ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Product_varients)