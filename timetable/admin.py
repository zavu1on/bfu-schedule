from django.contrib import admin
from .models import InstituteModel, DirectionModel, GroupModel, TeacherModel, PairTimetableModel
# Register your models here.


admin.site.register(InstituteModel)
admin.site.register(DirectionModel)
admin.site.register(GroupModel)
admin.site.register(TeacherModel)


@admin.register(PairTimetableModel)
class PairTimetableAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'teacher', 'start_time', 'date')
    search_fields = ('title', 'group__name', 'teacher__name')
    ordering = ['date']
