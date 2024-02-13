from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, hod_views, staff_views, student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),

    # login and logout
    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),

    # HOD PANEL
    path('hod/home', hod_views.HOME, name='hod_home'),
    # student
    path('hod/student/add', hod_views.Add_Student, name='add_student'),
    path('hod/student/view', hod_views.View_Student, name='view_student'),
    path('hod/student/edit/<str:pk>', hod_views.EDIT_STUDENT, name='edit_student'),
    path('hod/student/update', hod_views.UPDATE_STUDENT, name='update_student'),
    path('hod/student/delete/<str:admin>', hod_views.DELETE_STUDENT, name='delete_student'),
    # staff
    path('hod/staff/add', hod_views.ADD_STAFF, name='add_staff'),
    path('hod/staff/view', hod_views.VIEW_STAFF, name='view_staff'),
    path('hod/staff/view/<str:pk>', hod_views.EDIT_STAFF, name='edit_staff'),
    path('hod/staff/update', hod_views.UPDATE_STAFF, name='update_staff'),
    path('hod/staff/delete/<str:admin>', hod_views.DELETE_STAFF, name='delete_staff'),
    # course
    path('hod/course/add', hod_views.ADD_COURSE, name='add_course'),
    path('hod/course/view', hod_views.VIEW_COURSE, name='view_course'),
    path('hod/course/edit/<str:pk>', hod_views.EDIT_COURSE, name='edit_course'),
    path('hod/course/update', hod_views.UPDATE_COURSE, name='update_course'),
    path('hod/course/delete/<str:pk>', hod_views.DELETE_COURSE, name='delete_course'),
    # subject
    path('hod/subject/add', hod_views.ADD_SUBJECT, name='add_subject'),
    path('hod/subject/view', hod_views.VIEW_SUBJECT, name='view_subject'),
    path('hod/subject/edit/<str:pk>', hod_views.EDIT_SUBJECT, name='edit_subject'),
    path('hod/subject/update', hod_views.UPDATE_SUBJECT, name='update_subject'),
    path('hod/subject/delete/<str:pk>', hod_views.DELETE_SUBJECT, name='delete_subject'),
    # session
    path('hod/session/add', hod_views.ADD_SESSION, name='add_session'),
    path('hod/session/view', hod_views.VIEW_SESSION, name='view_session'),
    path('hod/session/edit/<str:pk>', hod_views.EDIT_SESSION, name='edit_session'),
    path('hod/session/update', hod_views.UPDATE_SESSION, name='update_Session'),
    path('hod/session/delete/<str:pk>', hod_views.DELETE_SESSION, name='delete_session'),
    # staff notifications
    path('hod/staff/send_notification', hod_views.STAFF_NOTIFICATION, name='send_staff_notification'),
    path('hod/staff/save_notification', hod_views.SAVE_STAFF_NOTIFICATION, name='save_staff_notification'),
    # student notification
    path('hod/student/send_notification', hod_views.STUDENT_NOTIFICATION, name='send_student_notification'),
    path('hod/student/save_notification', hod_views.SAVE_STUDENT_NOTIFICATION, name='save_student_notification'),
    # staff leave
    path('hod/staff/leave_view', hod_views.STAFF_LEAVE_VIEW, name='staff_leave_view'),
    path('hod/staff/approve_leave/<str:pk>', hod_views.APPROVE_STAFF_LEAVE, name='approve_staff_leave'),
    path('hod/staff/disapprove_leave/<str:pk>', hod_views.DISAPPROVE_STAFF_LEAVE, name='disapprove_staff_leave'),
    # staff feedback
    path('hod/staff/feedback', hod_views.STAFF_FEEDBACK, name='staff_feedback_reply'),
    path('hod/staff/feedback/save', hod_views.STAFF_FEEDBACK_SAVE, name='staff_feedback_reply_save'),
    # student feedback
    path('hod/student/feedback', hod_views.STUDENT_FEEDBACK, name='get_student_feedback'),
    path('hod/student/feedback/save', hod_views.STUDENT_FEEDBACK_SAVE, name='student_feedback_reply_save'),
    # student leave
    path('hod/student/leave_view', hod_views.STUDENT_LEAVE_VIEW, name='student_leave_view'),
    path('hod/student/approve_leave/<str:pk>', hod_views.APPROVE_STUDENT_LEAVE, name='approve_student_leave'),
    path('hod/student/disapprove_leave/<str:pk>', hod_views.DISAPPROVE_STUDENT_LEAVE, name='disapprove_student_leave'),
    # attendance
    path('hod/attendance', hod_views.VIEW_ATTENDANCE, name='view_attendance'),
    path('hod/teacher_attendance', hod_views.TEACHER_ATTENDANCE, name='teacher_attendance'),
    path('hod/take_teacher_attendance', hod_views.TAKE_TEACHER_ATTENDANCE, name='take_teacher_attendance'),
    path('hod/view_teacher_attendance', hod_views.VIEW_TEACHER_ATTENDANCE, name='view_teacher_attendance'),
    # schedule
    path('hod/schedule', hod_views.SCHEDULE, name='schedule'),
    path('hod/schedule/assign', hod_views.SCHEDULE_ASSIGN, name='schedule_assign'),
    path('hod/schedule/edit/<str:pk>', hod_views.EDIT_SCHEDULE, name='edit_schedule'),
    path('hod/schedule/update/<str:pk>', hod_views.UPDATE_SCHEDULE, name='update_schedule'),
    path('hod/schedule/delete/<str:pk>', hod_views.DELETE_SCHEDULE, name='delete_schedule'),
    # check result
    path('hod/check_result', hod_views.CHECK_RESULT, name='check_result'),
    # paper
    path('hod/papers', hod_views.SEE_PAPERS, name='see_paper'),
    path('hod/papers/check/<str:pk>', hod_views.CHECK_PAPERS, name='check_papers'),
    path('hod/papers/pdf/<int:pk>', hod_views.PDF, name='pdf'),
    # noticeboard
    path('hod/noticeboard/student', hod_views.NOTICE_BOARD_STUDENT, name='notice_board_student'),
    path('hod/noticeboard/staff', hod_views.NOTICE_BOARD_STAFF, name='notice_board_staff'),
    path('hod/noticeboard/delete/<str:pk>', hod_views.DELETE_STAFF_NOTICE, name='delete_staff_notice'),
    path('hod/noticeboard/delete_std/<str:pk>', hod_views.DELETE_STUDENT_NOTICE, name='delete_student_notice'),
    # fee
    path('hod/fee_structure', hod_views.FEE_STRUCTURE, name='fee_structure'),
    path('hod/invoice/<str:pk>', hod_views.INVOICE, name='invoice'),
    # student support
    path('hod/support_student/<str:pk>', hod_views.SUPPORT_STUDENT, name='support_student'),
    path('hod/support_student_list', hod_views.SUPPORT_STUDENT_LIST, name='support_student_list'),
    path('hod/support_student_list_delete/<str:pk>', hod_views.DELETE_SUPPORT_STUDENT_LIST, name='delete_support_student_list'),
    path('hod/student_support_reply/<str:pk>', hod_views.SUPPORT_STUDENT_REPLY, name='support_student_reply'),
    # payroll
    path('hod/payroll', hod_views.PAYROLL, name='payroll'),


    # STAFF PANEL
    path('staff/home', staff_views.HOME, name='staff_home'),
    path('staff/notifications', staff_views.NOTIFICATIONS, name='notifications'),
    path('staff/mark_as_done/<str:status>', staff_views.STAFF_NOTIFICATION_MARK_AS_DONE, name='staff_notification_mark_as_done'),
    path('staff/apply_leave', staff_views.STAFF_APPLY_LEAVE, name='staff_apply_leave'),
    path('staff/staff_apply_leave_send', staff_views.STAFF_APPLY_LEAVE_SEND, name='staff_apply_leave_send'),
    path('staff/Feedback', staff_views.STAFF_FEEDBACK, name='staff_feedback'),
    path('staff/feedback_save', staff_views.STAFF_FEEDBACK_SAVE, name='staff_feedback_save'),
    path('staff/take_attendance', staff_views.TAKE_STAFF_ATTENDANCE, name='take_staff_attendance'),
    path('staff/save_attendance', staff_views.STAFF_SAVE_ATTENDANCE, name='staff_save_attendance'),
    path('staff/view_attendance', staff_views.STAFF_VIEW_ATTENDANCE, name='staff_view_attendance'),
    path('staff/add/result', staff_views.ADD_RESULT, name='add_result'),
    path('staff/save/result', staff_views.SAVE_RESULT, name='staff_save_result'),
    path('staff/stats', staff_views.STAFF_STATS, name='staff_stats'),
    path('staff/stats/student_profile/<str:pk>', staff_views.STUDENT_PROFILE, name='student_profile'),
    path('staff/video_lectures_upload', staff_views.VIDEO_LECTURES, name='video_lectures_upload'),
    path('staff/video_lectures/add_topic', staff_views.ADD_TOPIC, name='add_topic'),
    path('staff/video_lectures/delete_topic/<str:pk>', staff_views.DELETE_TOPIC, name='delete_topic'),
    path('staff/video_lectures/update_topic_page/<str:pk>', staff_views.UPDATE_TOPIC_PAGE, name='update_topic_page'),
    path('staff/video_lectures/update_topic/<str:pk>', staff_views.UPDATE_TOPIC, name='update_topic'),
    # path('staff/video_lectures_upload/student_video', staff_views.STUDENT_VIDEO, name='student_video'),
    path('staff/diary', staff_views.DIARY, name='diary'),
    path('staff/diary/add_diary', staff_views.ADD_DIARY, name='add_diary'),
    path('staff/check_schedule', staff_views.CHECK_SCHEDULE, name='check_schedule'),
    path('staff/papers', staff_views.PAPERS, name='papers'),
    path('staff/papers/view', staff_views.VIEW_PAPER, name='view_paper'),
    path('staff/papers/edit/<str:pk>', staff_views.EDIT_PAPER, name='edit_paper'),
    path('staff/papers/update/<str:pk>', staff_views.UPDATE_PAPER, name='update_paper'),
    path('staff/noticeboard', staff_views.NOTICEBOARD, name='staff_noticeboard'),

    # STUDENT PANEL
    path('student/home', student_views.HOME, name='student_home'),
    path('student/notifications', student_views.NOTIFICATIONS, name='student_notifications'),
    path('student/mark_as_done/<str:status>', student_views.STUDENT_NOTIFICATION_MARK_AS_DONE, name='student_notification_mark_as_done'),
    path('student/feedback', student_views.STUDENT_FEEDBACK, name='student_feedback'),
    path('student/feedback_save', student_views.STUDENT_FEEDBACK_SAVE, name='student_feedback_save'),
    path('student/apply_leave', student_views.STUDENT_LEAVE, name='student_apply_leave'),
    path('student/apply_leave_send', student_views.STUDENT_LEAVE_SEND, name='student_apply_leave_send'),
    path('student/view_attendance', student_views.STUDENT_VIEW_ATTENDANCE, name='student_view_attendance'),
    path('student/view_result', student_views.VIEW_RESULT, name='view_result'),
    path('student/view_diary', student_views.VIEW_DIARY, name='view_diary'),
    path('student/view_diary/check_diary/<int:subject_id>/<str:diary_date>', student_views.CHECK_DIARY, name='check_diary'),
    path('student/video_lectures', student_views.VIDEO_LECTURE, name='video_lecture'),
    path('student/class_timetable', student_views.CLASS_TIMETABLE, name='class_timetable'),
    path('student/noticeboard', student_views.NOTICEBOARD, name='noticeboard'),
    path('student/student_support', student_views.STUDENT_SUPPORT, name='student_support'),
    path('student/inbox', student_views.INBOX, name='inbox'),
    path('student/support_reply/<int:pk>', student_views.SUPPORT_REPLY, name='support_reply'),
    path('student/inbox_delete/<int:pk>', student_views.INBOX_DELETE, name='inbox_delete'),
    path('student/fees', student_views.FEES, name='fees'),
    path('student/generate_pdf/', student_views.GENERATE_PDF, name='generate_pdf'),

    # profile
    path('profile', views.PROFILE, name='profile'),
    path('profile/update', views.PROFILE_UPDATE, name='profile_update')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)