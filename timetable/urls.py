from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('api/add_timetable/', views.AddTimetableView.as_view()),
    path('get_timetable/', views.get_timetable_view),
    path('', views.AbitsTimetableView.as_view()),
    path('teachers/', views.TeacherTimetableView.as_view()),
    path('timetable/<str:group_or_teacher>/<str:date>/', views.FindTimetableView.as_view(), name='find_timetable'),
    path('month-table/', views.ChooseGroupForMonthTableView.as_view(), name='choose_group_for_table'),
    path('month-table/<str:group>/', views.MonthTableView.as_view(), name='month_timetable'),
]
