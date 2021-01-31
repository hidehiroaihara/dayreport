from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import Profile, Department, Position, Employee 
from diary.models import Category, CategoryList, File, Done


class ProfileInline(admin.StackedInline):
  model = Profile
  max_num = 1
  can_delete = False

class EmployeeInline(admin.StackedInline):
  model = Employee
  max_num = 1
  can_delete = False

class UserAdmin(AuthUserAdmin):
  inlines = [ProfileInline, EmployeeInline ]
  # EmploymentInline

class FileInline(admin.StackedInline):
  model = File
  extra = 3

class DoneAdmin(admin.ModelAdmin):
  inlines = [FileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Category)
admin.site.register(CategoryList)
admin.site.register(Done, DoneAdmin)
admin.site.register(File)


