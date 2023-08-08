from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Loan,Book

# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'age', 'city')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'age', 'city'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Loan)
admin.site.register(Book)