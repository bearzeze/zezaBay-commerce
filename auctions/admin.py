from django.contrib import admin
from .models import Bid, Comment, Item, Category, Watchlist

class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_by", "active")
    
    @admin.display(ordering='created_by', description='seller')
    def get_seller(self, obj):
        return obj.created_by


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )

# Register your models here.
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)

