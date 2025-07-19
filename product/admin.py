from django.contrib import admin
from .models import Category, Product, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    search_fields = 'title'.split()
    list_filter = 'category'.split()    
    list_display = 'title price category'.split()
    list_editable = 'category'.split()
    inlines = [ReviewInline] 

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
