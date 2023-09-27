from django.contrib import admin
from .models import *




# registering models 




class ProductImageAdmin(admin.StackedInline):
    model =ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageAdmin]



admin.site.register(Brand)
admin.site.register(Product , ProductAdmin)
admin.site.register(ProductImage)