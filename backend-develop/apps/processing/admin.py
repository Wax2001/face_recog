from django.contrib import admin
from apps.processing.models import *

# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image
    extra = 5
    insert_after = 'role'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'available',
    )
    list_display_links = (
        'id',
        'username',
    )
    
    fields = ('username', 'first_name', 'last_name', 'email', 'role',)
    inlines = [ImageInline,]

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'check_in_time',
        'check_out_time',
        'late_arrive_time',
        'early_leave_time',
        'available',
    )
    list_display_links = (
        'id',
        'user',
    )

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'img',
        'available',
    )
    list_display_links = (
        'id',
        'user',
    )

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'start_time',
        'break_time_start',
        'break_time_end',
        'end_time',
    )
    list_display_links = (
        'id',
        'user',
    )

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_work_hours',
        'hourly_rate',
        'allowance',
    )
    list_display_links = (
        'id',
        'user',
    )