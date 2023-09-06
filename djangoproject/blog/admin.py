from django.contrib import admin
from .models import *


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    

admin.site.register(Account)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
