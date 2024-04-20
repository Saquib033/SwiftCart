from django.contrib import admin

# Register your models here.

from .models import *


class Product_Images(admin.TabularInline):
    
    model = Product_Image

class Additional_Informations(admin.TabularInline):
    
    model = Additional_Information
    
class Product_Admin(admin.ModelAdmin):
    
    inlines = (Product_Images, Additional_Informations)
    list_display = ('product_name','price','Categories','color','section')
    list_editable = ('Categories','section','color')


admin.site.register(Section)
admin.site.register(Product, Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
admin.site.register(Brand)
admin.site.register(slider)
admin.site.register(banner_area)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Color)
admin.site.register(Cupon)