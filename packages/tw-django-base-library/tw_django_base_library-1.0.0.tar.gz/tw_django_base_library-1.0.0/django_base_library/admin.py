from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from import_export.admin import ImportExportModelAdmin
from authentication.models import User

class AdminLogging(ImportExportModelAdmin,admin.ModelAdmin):

    readonly_fields = ('created_By', 'updated_By', 'created_at', 'updated_at')

    exclude = ('created_by', 'updated_by')
    
    def save_model(self, request, obj, form, change):
        
        if obj.created_by: 
            obj.updated_by = request.user.id
        else:
            obj.created_by = request.user.id
            obj.updated_by = request.user.id

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return self.model.objects.get_queryset('all').all()

    def created_By(self,obj):
        if obj.created_by != None:
            user_obj = User.objects.get_queryset('all').get(id=obj.created_by)
            return user_obj.username

    def updated_By(self,obj):
        if obj.updated_by != None:
            user_obj = User.objects.get_queryset('all').get(id=obj.updated_by)
            return user_obj.username


class ApplicationLogging(ImportExportModelAdmin,admin.ModelAdmin):

    readonly_fields = ('created_By', 'updated_By', 'created_at', 'updated_at')

    exclude = ('created_by', 'updated_by')

    def get_queryset(self, request):
        return self.model.objects.get_queryset('all').all()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def created_By(self,obj):
        if obj.created_by != None:
            user_obj = User.objects.get_queryset('all').get(id=obj.created_by)
            return user_obj.username

    def updated_By(self,obj):
        if obj.updated_by != None:
            user_obj = User.objects.get_queryset('all').get(id=obj.updated_by)
            return user_obj.username
