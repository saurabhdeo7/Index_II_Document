from django.contrib import admin
from .models import IndexIIdoc
# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_filter = ('added_by', 'serialNo')

admin.site.register(IndexIIdoc,DocumentAdmin)