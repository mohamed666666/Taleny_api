

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserBase
from .models.talent import Talent,Talentee
from .models.Skill import Skill,skilled_in
from .models.investgator import Investgator 
from .models.admin import TheAdmin ,ContactRequest
from .models.follow import Follow


admin.site.register(Talent)
admin.site.register(Talentee)


admin.site.register(Skill)
admin.site.register(skilled_in)

admin.site.register(TheAdmin)
admin.site.register(ContactRequest)

admin.site.register(Investgator)


admin.site.register(Follow)





class UserBaseAdmin(UserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ('email', 'user_name', 'full_name', 'is_staff', 'is_active','profile_image','phone_number')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'title', 'about', 'age', 'profile_image', 'phone_number', 'government', 'area')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created', 'updated')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name','profile_image', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'user_name')
    ordering = ('email',)

# Register the UserBase model with the custom admin configuration
admin.site.register(UserBase, UserBaseAdmin)

