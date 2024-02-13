from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username', 'user_type']


admin.site.register(CustomUser, UserModel)
admin.site.register(Course)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Staff_Notification)
admin.site.register(Staff_Leave)
admin.site.register(Staff_Feedback)
admin.site.register(Student_Notification)
admin.site.register(Student_Feedback)
admin.site.register(Student_Leave)
admin.site.register(Attendance)
admin.site.register(Attendance_Report)
admin.site.register(Student_Result)
admin.site.register(Syllabus)
admin.site.register(Diary)
admin.site.register(Schedule)
admin.site.register(Staff_Attendance)
admin.site.register(ExamPaper)
admin.site.register(NoticeBoard_Students)
admin.site.register(NoticeBoard_Teachers)
admin.site.register(Student_Support)
admin.site.register(Student_Support_Reply)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
