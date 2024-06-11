from django.contrib import admin

from base_app.models import (
    ApplicationUser,
    RenterUser,
    RenterRegisterRequests,
    AdminUser,
    RenterRegisterResults,
)


@admin.register(ApplicationUser)
class ApplicationUserAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_renter",
    ]


@admin.register(RenterUser)
class RenterUserAdmin(admin.ModelAdmin):
    list_display = ["renter_id", "application_user"]


@admin.register(RenterRegisterRequests)
class RenterRegisterRequestsAdmin(admin.ModelAdmin):
    list_display = [
        "reference_id",
        "application_user",
        "is_reviewed",
        "data_generated_on",
    ]


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ["admin_id", "application_user"]


@admin.register(RenterRegisterResults)
class RenterRegisterResultsAdmin(admin.ModelAdmin):
    list_display = [
        "reference_id",
        "data_generated_on",
        "is_approved",
        "reviewed_by",
        "renter_request",
    ]
