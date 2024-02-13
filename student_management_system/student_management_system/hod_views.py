from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from schoolsystem.models import Course, Session_Year, CustomUser, Student, Staff, Subject, Staff_Notification, \
    Staff_Leave, Staff_Feedback, Student_Notification, Student_Feedback, Student_Leave, Attendance, Attendance_Report, \
    Schedule, Student_Result, Staff_Attendance, ExamPaper, NoticeBoard_Students, NoticeBoard_Teachers, Student_Support, \
    Student_Support_Reply, Invoice, InvoiceItem
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Count
from datetime import datetime
import uuid
from django.db.models import Max
from django.core.cache import cache


@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()

    context = {
        'student_count': student_count,
        'staff_count': staff_count,
        'course_count': course_count,
        'subject_count': subject_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
    }

    return render(request, 'hod/home.html', context)


@login_required(login_url='/')
def Add_Student(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        profile_pic = request.FILES.get('profile_pic')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken!')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken!')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            student = Student(
                admin=user,
                address=address,
                session_year_id=session_year,
                course_id=course,
                gender=gender,
            )
            student.save()
            messages.success(request, user.first_name + " " + user.last_name + ' is successfully added!')
            return redirect('add_student')

    context = {
        "course": course,
        "session_year": session_year,
    }

    return render(request, 'hod/add_student.html', context)


@login_required(login_url='/')
def View_Student(request):
    student = Student.objects.all()
    context = {
        'student': student,
    }

    return render(request, 'hod/view_student.html', context)


@login_required(login_url='/')
def EDIT_STUDENT(request, pk):
    student = Student.objects.filter(id=pk)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    context = {
        'student': student,
        'course': course,
        'session_year': session_year,
    }

    return render(request, 'hod/edit_student.html', context)


@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        profile_pic = request.FILES.get('profile_pic')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        user = CustomUser.objects.get(id=student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        if password is not None and password is not "":
            user.set_password(password)
        if profile_pic is not None and profile_pic is not "":
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin=student_id)

        student.address = address
        student.gender = gender

        course = Course.objects.get(id=course_id)
        student.course_id = course

        session_year = Session_Year.objects.get(id=session_year_id)
        student.session_year_id = session_year

        student.save()
        messages.success(request, 'Record is successfully updated!')
        return redirect('view_student')

    return render(request, 'hod/edit_student.html')


@login_required(login_url='/')
def DELETE_STUDENT(request, admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.success(request, 'Record has been deleted successfully!')

    return redirect('view_student')


@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')

        course = Course(
            name=course_name,
        )
        course.save()
        messages.success(request, 'Course Added Successfully!')
        return redirect('add_course')

    return render(request, 'hod/add_course.html')


@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()

    context = {
        'course': course,
    }

    return render(request, 'hod/view_course.html', context)


@login_required(login_url='/')
def EDIT_COURSE(request, pk):
    course = Course.objects.get(id=pk)

    context = {
        'course': course,
    }

    return render(request, 'hod/edit_course.html', context)


@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')

        course = Course.objects.get(id=course_id)

        course.name = course_name
        course.save()
        messages.success(request, 'Course Updated Successfully!')
        return redirect('view_course')

    return render(request, 'hod/edit_course.html')


@login_required(login_url='/')
def DELETE_COURSE(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    messages.success(request, 'Course Deleted Successfully!')
    return redirect('view_course')


@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        profile_pic = request.FILES.get('profile_pic')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken!')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken!')
            return redirect('add_staff')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=2
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                address=address,
                gender=gender
            )
            staff.save()
            messages.success(request, 'Staff Successfully Added!')
            return redirect('add_staff')

    return render(request, 'hod/add_staff.html')


@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()

    context = {
        'staff': staff,
    }

    return render(request, 'hod/view_staff.html', context)


@login_required(login_url='/')
def EDIT_STAFF(request, pk):
    staff = Staff.objects.get(id=pk)

    context = {
        'staff': staff,
    }

    return render(request, 'hod/edit_staff.html', context)


@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        profile_pic = request.FILES.get('profile_pic')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        user = CustomUser.objects.get(id=staff_id)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        if password is not None and password is not "":
            user.set_password(password)
        if profile_pic is not None and profile_pic is not "":
            user.profile_pic = profile_pic
        user.save()

        staff = Staff.objects.get(admin=staff_id)

        staff.address = address
        staff.gender = gender
        staff.save()
        messages.success(request, 'Staff Updated Successfully!')
        return redirect('view_staff')

    return render(request, 'hod/edit_staff.html')


@login_required(login_url='/')
def DELETE_STAFF(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, 'Record has been deleted successfully!')

    return redirect('view_staff')


@login_required(login_url='/')
def ADD_SUBJECT(request):
    course = Course.objects.all()
    staff = Staff.objects.all()

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            name=subject_name,
            course=course,
            staff=staff,
        )
        subject.save()
        messages.success(request, 'Subject Has Been Added!')
        return redirect('add_subject')

    context = {
        'course': course,
        'staff': staff
    }

    return render(request, 'hod/add_subject.html', context)


@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all()

    context = {
        'subject': subject,
    }

    return render(request, 'hod/view_subject.html', context)


@login_required(login_url='/')
def EDIT_SUBJECT(request, pk):
    subject = Subject.objects.get(id=pk)
    course = Course.objects.all()
    staff = Staff.objects.all()

    context = {
        'subject': subject,
        'course': course,
        'staff': staff,
    }

    return render(request, 'hod/edit_subject.html', context)


@login_required(login_url='/')
def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        subject_id = request.POST.get('subject_id')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        # subject = Subject(
        #     id=subject_id,
        #     name=subject_name,
        #     course=course,
        #     staff=staff,
        # )
        subject = get_object_or_404(Subject, id=subject_id)

        # Update the subject fields
        subject.name = subject_name
        subject.course = course
        subject.staff = staff
        subject.save()
        messages.success(request, 'Subject Successfully Updated!')
        return redirect('view_subject')


@login_required(login_url='/')
def DELETE_SUBJECT(request, pk):
    subject = Subject.objects.filter(id=pk)
    subject.delete()
    messages.success(request, 'Subject has been deleted successfully!')

    return redirect('view_subject')


@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == "POST":
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            session_start=session_year_start,
            session_end=session_year_end,
        )
        session.save()
        messages.success(request, 'Session Added Successfully!')
        return redirect('add_session')

    return render(request, 'hod/add_session.html')


@login_required(login_url='/')
def VIEW_SESSION(request):
    session = Session_Year.objects.all()

    context = {
        'session': session,
    }

    return render(request, 'hod/view_session.html', context)


@login_required(login_url='/')
def EDIT_SESSION(request, pk):
    session = Session_Year.objects.filter(id=pk)

    context = {
        'session': session,
    }

    return render(request, 'hod/edit_session.html', context)


@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == "POST":
        session_year_id = request.POST.get('session_year_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            id=session_year_id,
            session_start=session_year_start,
            session_end=session_year_end,
        )
        session.save()
        messages.success(request, 'Session Updated Successfully!')
        return redirect('view_session')


@login_required(login_url='/')
def DELETE_SESSION(request, pk):
    session = Session_Year.objects.get(id=pk)
    session.delete()
    messages.success(request, 'Session Deleted Successfully!')

    return redirect('view_session')


@login_required(login_url='/')
def STAFF_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]

    context = {
        'staff': staff,
        'see_notification': see_notification,
    }

    return render(request, 'hod/staff_notification.html', context)


@login_required(login_url='/')
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin=staff_id)

        notification = Staff_Notification(
            staff_id=staff,
            message=message,
        )
        notification.save()
        messages.success(request, 'Message Send Successfully!')
        return redirect('send_staff_notification')


@login_required(login_url='/')
def STAFF_LEAVE_VIEW(request):
    staff_leave = Staff_Leave.objects.all()

    context = {
        'staff_leave': staff_leave,
    }

    return render(request, 'hod/staff_leave.html', context)


@login_required(login_url='/')
def APPROVE_STAFF_LEAVE(request, pk):
    leave = Staff_Leave.objects.get(id=pk)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')


@login_required(login_url='/')
def DISAPPROVE_STAFF_LEAVE(request, pk):
    leave = Staff_Leave.objects.get(id=pk)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')


def STUDENT_LEAVE_VIEW(request):
    student_leave = Student_Leave.objects.all()

    context = {
        'student_leave': student_leave,
    }

    return render(request, 'hod/student_leave.html', context)


def APPROVE_STUDENT_LEAVE(request, pk):
    leave = Student_Leave.objects.get(id=pk)
    leave.status = 1
    leave.save()
    return redirect('student_leave_view')


def DISAPPROVE_STUDENT_LEAVE(request, pk):
    leave = Student_Leave.objects.get(id=pk)
    leave.status = 2
    leave.save()
    return redirect('student_leave_view')


def STAFF_FEEDBACK(request):
    feedback = Staff_Feedback.objects.all()
    feedback_history = Staff_Feedback.objects.all().order_by('-id')[0:5]

    context = {
        'feedback': feedback,
        'feedback_history': feedback_history,
    }

    return render(request, 'hod/staff_feedback.html', context)


def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_Feedback.objects.get(id=feedback_id)

        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        messages.success(request, 'Replied!')
        return redirect('staff_feedback_reply')


def STUDENT_FEEDBACK(request):
    feedback = Student_Feedback.objects.all()
    feedback_history = Student_Feedback.objects.all().order_by('-id')[0:5]

    context = {
        'feedback': feedback,
        'feedback_history': feedback_history,
    }

    return render(request, 'hod/student_feedback.html', context)


def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Student_Feedback.objects.get(id=feedback_id)

        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        messages.success(request, 'Replied!')
        return redirect('get_student_feedback')


def STUDENT_NOTIFICATION(request):
    student = Student.objects.all()
    notification = Student_Notification.objects.all()

    context = {
        'student': student,
        'notification': notification,
    }

    return render(request, 'hod/student_notification.html', context)


def SAVE_STUDENT_NOTIFICATION(request):
    if request.method == "POST":
        message = request.POST.get('message')
        student_id = request.POST.get('student_id')

        student = Student.objects.get(admin=student_id)

        student_notification = Student_Notification(
            student_id=student,
            message=message,
        )
        student_notification.save()
        messages.success(request, 'Message Send Successfully!')
        return redirect('send_student_notification')


def VIEW_ATTENDANCE(request):
    subject = Subject.objects.all()
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None

    if action is not None:
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date)
        for i in attendance:
            attendance_id = i.id
            attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'attendance_date': attendance_date,
        'attendance_report': attendance_report,
    }

    return render(request, 'hod/view_attendance.html', context)


def TEACHER_ATTENDANCE(request):
    staff = Staff.objects.all()

    context = {
        'staff': staff,
    }

    return render(request, 'hod/teacher_attendance.html', context)


def TAKE_TEACHER_ATTENDANCE(request):
    if request.method == "POST":
        attendance_date = request.POST.get('attendance_date')
        staff_id = request.POST.getlist('staff_id')

        for i in staff_id:
            stf_id = i
            int_stf = int(stf_id)

            present_staffs = Staff.objects.get(id=int_stf)

            attendance_report = Staff_Attendance(
                attendance_date=attendance_date,
                staff_id=present_staffs,
            )
            attendance_report.save()

    return redirect('teacher_attendance')


def VIEW_TEACHER_ATTENDANCE(request):
    action = request.GET.get('action')

    attendance_date = None
    attendance = None

    if action is not None:
        attendance_date = request.POST.get('attendance_date')

        attendance = Staff_Attendance.objects.filter(attendance_date=attendance_date)

    context = {
        'action': action,
        'attendance_date': attendance_date,
        'attendance': attendance,
    }

    return render(request, 'hod/view_teacher_attendance.html', context)


def SCHEDULE(request):
    subject = Subject.objects.all()
    action = request.GET.get('action')

    get_subject = None
    staff = None
    schedule = None

    if action is not None:
        subject_id = request.POST.get('subject_id')

        get_subject = Subject.objects.get(id=subject_id)
        staff = Staff.objects.all()

        schedule = Schedule.objects.filter(subject=get_subject)

    context = {
        'subject': subject,
        'action': action,
        'staff': staff,
        'get_subject': get_subject,
        'schedule': schedule,
    }

    return render(request, 'hod/schedule.html', context)


def SCHEDULE_ASSIGN(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        staff_id = request.POST.get('staff_id')
        sch_date = request.POST.get('sch_date')
        sch_time = request.POST.get('sch_time')
        end_time = request.POST.get('end_time')
        sch_room = request.POST.get('sch_room')

        subject = Subject.objects.get(id=subject_id)
        staff = Staff.objects.get(admin=staff_id)

        schedule = Schedule(
            subject=subject,
            staff=staff,
            assign_date=sch_date,
            assign_time=sch_time,
            end_time=end_time,
            room_no=sch_room,
        )
        messages.success(request, 'Schedule Assigned!')
        schedule.save()

        return redirect('schedule')


def EDIT_SCHEDULE(request, pk):
    schedule = Schedule.objects.get(id=pk)

    context = {
        'schedule': schedule,
    }

    return render(request, 'hod/edit_schedule.html', context)


def UPDATE_SCHEDULE(request, pk):
    if request.method == "POST":
        sch_date = request.POST.get('sch_date')
        sch_time = request.POST.get('sch_time')
        end_time = request.POST.get('end_time')
        sch_room = request.POST.get('sch_room')

        schedule = Schedule.objects.get(id=pk)

        schedule.assign_date = sch_date
        schedule.assign_time = sch_time
        schedule.end_time = end_time
        schedule.room_no = sch_room
        messages.success(request, 'Schedule is successfully updated!')
        schedule.save()

    return redirect('schedule')


def DELETE_SCHEDULE(request, pk):
    schedule = Schedule.objects.get(id=pk)
    schedule.delete()

    return redirect('schedule')


def CHECK_RESULT(request):
    subjects = Subject.objects.all()
    action = request.GET.get('action')

    get_subject = None
    results = None

    if action is not None:
        subject_id = request.POST.get('subject_id')

        get_subject = Subject.objects.get(id=subject_id)
        results = Student_Result.objects.filter(subject_id=get_subject)

        for result in results:
            total_marks = (
                    result.assignment_marks + result.assignment_2 + result.assignment_3 + result.assignment_4 +
                    result.exam_marks + result.mid_term + result.class_activity_1 + result.class_activity_2 +
                    result.quiz_1 + result.quiz_2 + result.quiz_3 + result.quiz_4
            )
            result.total_marks = total_marks

    context = {
        'subjects': subjects,
        'action': action,
        'get_subject': get_subject,
        'results': results,
    }

    return render(request, 'hod/check_result.html', context)


def SEE_PAPERS(request):
    subjects = Subject.objects.all()
    papers = ExamPaper.objects.all()

    context = {
        'subjects': subjects,
        'papers': papers,
    }

    return render(request, 'hod/paper.html', context)


def CHECK_PAPERS(request, pk):
    paper = ExamPaper.objects.get(id=pk)

    context = {
        'paper': paper,
    }

    return render(request, 'hod/check_paper.html', context)


def PDF(request, pk):
    try:
        paper = ExamPaper.objects.get(id=pk)
    except ExamPaper.DoesNotExist:
        return HttpResponse("Paper not found", status=404)

        # Your school name and page title
    school_name = "ABC School"
    page_title = "Paper Details"

    context = {
        'school_name': school_name,
        'page_title': page_title,
        'paper': paper,
    }

    template = get_template('hod/pdf.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="paper_{pk}.pdf"'

    pdf = pisa.CreatePDF(html, dest=response)

    if not pdf.err:
        return response

    return HttpResponse("Error generating PDF", status=500)


def NOTICE_BOARD_STUDENT(request):
    if request.method == "POST":
        notice = request.POST.get('notice')

        noticeboard = NoticeBoard_Students(
            students_board=notice,
        )
        messages.success(request, 'Notice Placed on NoticeBoard!')
        noticeboard.save()
        return redirect('notice_board_student')

    notices = NoticeBoard_Students.objects.all()
    context = {
        'notices': notices,
    }

    return render(request, 'hod/notice_board_student.html', context)


def NOTICE_BOARD_STAFF(request):
    if request.method == "POST":
        notice = request.POST.get('notice')

        noticeboard = NoticeBoard_Teachers(
            teachers_board=notice,
        )
        messages.success(request, 'Notice Placed on NoticeBoard!')
        noticeboard.save()
        return redirect('notice_board_staff')

    notices = NoticeBoard_Teachers.objects.all()
    context = {
        'notices': notices,
    }

    return render(request, 'hod/notice_board_staff.html', context)


def DELETE_STAFF_NOTICE(request, pk):
    notice = NoticeBoard_Teachers.objects.get(id=pk)
    messages.error(request, 'Notice Deleted on NoticeBoard!')
    notice.delete()

    return redirect('notice_board_staff')


def DELETE_STUDENT_NOTICE(request, pk):
    notice = NoticeBoard_Students.objects.get(id=pk)
    messages.error(request, 'Notice Deleted on NoticeBoard!')
    notice.delete()

    return redirect('notice_board_student')


def SUPPORT_STUDENT(request, pk):
    support_student = Student_Support.objects.get(id=pk)

    context = {
        'support_student': support_student,
    }

    return render(request, 'hod/support_student.html', context)


def SUPPORT_STUDENT_LIST(request):
    support_student = Student_Support.objects.all()
    replies = Student_Support_Reply.objects.all()

    context = {
        'support_student': support_student,
        'replies': replies,
    }

    return render(request, 'hod/support_student_list.html', context)


def DELETE_SUPPORT_STUDENT_LIST(request, pk):
    support_student = Student_Support.objects.get(id=pk)
    support_student.delete()
    messages.success(request, 'You have Been Deleted Query!')

    return redirect('support_student_list')


def SUPPORT_STUDENT_REPLY(request, pk):
    support_student = Student_Support.objects.get(id=pk)

    if request.method == "POST":
        query_reply = request.POST.get('query_reply')
        # name = request.POST.get('name')

        support_reply = Student_Support_Reply(
            query_reply=query_reply,
            subject=support_student,
            # to=name,
        )
        messages.success(request, 'Reply Sent!')
        support_reply.save()
        return redirect('support_student_list')

    context = {
        'support_student': support_student,
    }

    return render(request, 'hod/student_support_reply.html', context)


def FEE_STRUCTURE(request):
    all_courses_with_students_count = Course.objects.annotate(student_count=Count('student'))

    context = {
        'all_courses_with_students_count': all_courses_with_students_count,
    }

    return render(request, 'hod/fee_structure.html', context)


def generate_serial_number(course_id):
    timestamp = int(datetime.timestamp(datetime.now()))
    unique_id = str(uuid.uuid4().int)[:8]
    return f'{course_id}_{timestamp}_{unique_id}'


def INVOICE(request, pk):
    course = Course.objects.get(id=pk)

    if request.method == 'POST':
        descriptions = []
        amounts = []

        for key, value in request.POST.items():
            if key.startswith('description_'):
                descriptions.append(value)
            elif key.startswith('amount_'):
                amounts.append(value)

        # Now 'descriptions' and 'amounts' contain the corresponding values

        # Generate a unique serial_number
        serial_number = generate_serial_number(course.id)

        # Check if the generated serial number is already in use
        while Invoice.objects.filter(serial_number=serial_number).exists():
            serial_number = generate_serial_number(course.id)

        # Create and save an Invoice object with the generated serial number
        invoice = Invoice(course=course, serial_number=serial_number)
        invoice.save()

        # Create and save InvoiceItem objects for each pair of description and amount
        for description, amount in zip(descriptions, amounts):
            item = InvoiceItem(invoice=invoice, description=description, amount=amount)
            item.save()

        messages.success(request, 'Invoice Created!')
        return redirect('fee_structure')

    context = {
        'course': course,
    }

    return render(request, 'hod/invoice.html', context)


def PAYROLL(request):
    return render(request, 'hod/payroll.html')
