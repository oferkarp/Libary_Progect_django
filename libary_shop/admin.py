from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
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


# class LoanAdmin(ModelAdmin):
#      readonly_fields = ['return_date']

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Loan,LoanAdmin)
admin.site.register(Loan)
admin.site.register(Book)
