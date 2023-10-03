from django.contrib import admin
from .models import *




# registering models 




class ProductImageAdmin(admin.StackedInline):
    model =ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','price']
    inlines=[ProductImageAdmin]

@admin.register(ColorVarient)
class ColorVarientAdmin(admin.ModelAdmin):
    list_display=['color_name','price']
    model= ColorVarient

@admin.register(RamVarient)
class RamVarientAdmin(admin.ModelAdmin):
    list_display=['ram_no','price']
    model= RamVarient

admin.site.register(Brand)
admin.site.register(Product , ProductAdmin)
admin.site.register(ProductImage)