from django.contrib import admin

# Register your models here.
from .models import ReleaseOrder


@admin.register(ReleaseOrder)
class ReleaseOrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "release_no",
        "app_code",
        "env_name",
        "branch_name",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "env_name",
    ]

    search_fields = [
        "release_no",
        "app_code",
        "env_name",
    ]
