import os.path
from django.conf import settings
from django.shortcuts import render, redirect
from schoolsystem.models import Staff, Staff_Notification, Staff_Leave, Staff_Feedback, Subject, Session_Year, Student, \
    Attendance, Attendance_Report, Student_Result, Syllabus, Diary, Schedule, ExamPaper, NoticeBoard_Teachers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter


@login_required(login_url='/')
def HOME(request):
    return render(request, 'staff/home.html')


@login_required(login_url='/')
def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id

        notification = Staff_Notification.objects.filter(staff_id=staff_id)

        context = {
            'notification': notification,
        }

    return render(request, 'staff/notifications.html', context)


@login_required(login_url='/')
def STAFF_NOTIFICATION_MARK_AS_DONE(request, status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('notifications')


@login_required(login_url='/')
def STAFF_APPLY_LEAVE(request):
    staff = Staff.objects.get(admin=request.user.id)
    staff_id = staff.id

    leave_history = Staff_Leave.objects.filter(staff_id=staff_id)

    context = {
        'leave_history': leave_history,
    }

    return render(request, 'staff/apply_leave.html', context)


@login_required(login_url='/')
def STAFF_APPLY_LEAVE_SEND(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff = Staff.objects.get(admin=request.user.id)

        leave = Staff_Leave(
            staff_id=staff,
            date=leave_date,
            message=leave_message,
        )
        leave.save()
        messages.success(request, 'Leave Sent!')
        return redirect('staff_apply_leave')


def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin=request.user.id)

    feedback_history = Staff_Feedback.objects.filter(staff_id=staff_id)

    context = {
        'feedback_history': feedback_history,
    }

    return render(request, 'staff/feedback.html', context)


def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')

        staff = Staff.objects.get(admin=request.user.id)
        feedback_staff = Staff_Feedback(
            staff_id=staff,
            feedback=feedback,
            feedback_reply="",
        )
        feedback_staff.save()
        messages.success(request, 'Feedback has been sent!')
        return redirect('staff_feedback')


def TAKE_STAFF_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin=request.user.id)

    subject = Subject.objects.filter(staff=staff_id)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    students = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)

            subject = Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'action': action,
        'students': students,
    }

    return render(request, 'staff/take_attendance.html', context)


def STAFF_SAVE_ATTENDANCE(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id=get_subject,
            session_year_id=get_session_year,
            attendance_date=attendance_date,
        )
        attendance.save()
        for i in student_id:
            std_id = i
            int_std = int(std_id)

            present_students = Student.objects.get(id=int_std)

            attendance_report = Attendance_Report(
                student_id=present_students,
                attendance_id=attendance,
            )
            attendance_report.save()
    return redirect('take_staff_attendance')


def STAFF_VIEW_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin=request.user.id)

    subject = Subject.objects.filter(staff=staff_id)
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

    return render(request, 'staff/view_attendance.html', context)


def ADD_RESULT(request):
    staff = Staff.objects.get(admin=request.user.id)

    subjects = Subject.objects.filter(staff=staff)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session = None
    students = None
    assignment_marks_1 = None
    assignment_marks_2 = None
    assignment_marks_3 = None
    assignment_marks_4 = None
    exam_marks = None
    mid_term = None
    class_activity_1 = None
    class_activity_2 = None
    quiz_1 = None
    quiz_2 = None
    quiz_3 = None
    quiz_4 = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subject.objects.get(id=subject_id)
            get_session = Session_Year.objects.get(id=session_year_id)

            subjects = Subject.objects.filter(id=subject_id)
            for i in subjects:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)

                # Retrieve the student result based on assignment marks
                student_result = Student_Result.objects.filter(
                    subject_id=get_subject,
                    assignment_marks__isnull=False
                ).first()

                # If an existing result is found, update assignment marks; otherwise, assign None
                if student_result:
                    assignment_marks_1 = student_result.assignment_marks
                    assignment_marks_2 = student_result.assignment_2
                    assignment_marks_3 = student_result.assignment_3
                    assignment_marks_4 = student_result.assignment_4
                    exam_marks = student_result.exam_marks
                    mid_term = student_result.mid_term
                    class_activity_1 = student_result.class_activity_1
                    class_activity_2 = student_result.class_activity_2
                    quiz_1 = student_result.quiz_1
                    quiz_2 = student_result.quiz_2
                    quiz_3 = student_result.quiz_3
                    quiz_4 = student_result.quiz_4

    context = {
        'subjects': subjects,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session,
        'students': students,
        'assignment_marks_1': assignment_marks_1,
        'assignment_marks_2': assignment_marks_2,
        'assignment_marks_3': assignment_marks_3,
        'assignment_marks_4': assignment_marks_4,
        'exam_marks': exam_marks,
        'mid_term': mid_term,
        'class_activity_1': class_activity_1,
        'class_activity_2': class_activity_2,
        'quiz_1': quiz_1,
        'quiz_2': quiz_2,
        'quiz_3': quiz_3,
        'quiz_4': quiz_4,
    }

    return render(request, 'staff/add_result.html', context)


def SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_1 = request.POST.get('assignment_1')
        assignment_2 = request.POST.get('assignment_2')
        assignment_3 = request.POST.get('assignment_3')
        assignment_4 = request.POST.get('assignment_4')
        exam_marks = request.POST.get('exam_mark')
        class_activity_1 = request.POST.get('class_activity_1')
        class_activity_2 = request.POST.get('class_activity_2')
        midterm = request.POST.get('midterm')
        quiz_1 = request.POST.get('quiz_1')
        quiz_2 = request.POST.get('quiz_2')
        quiz_3 = request.POST.get('quiz_3')
        quiz_4 = request.POST.get('quiz_4')

        get_subject = Subject.objects.get(id=subject_id)
        get_student = Student.objects.get(admin=student_id)

        check_exist = Student_Result.objects.filter(subject_id=get_subject, student_id=get_student).exists()

        if check_exist:
            result = Student_Result.objects.get(subject_id=get_subject, student_id=get_student)
            result.assignment_marks = assignment_1
            result.assignment_2 = assignment_2
            result.assignment_3 = assignment_3
            result.assignment_4 = assignment_4
            result.exam_marks = exam_marks
            result.mid_term = midterm
            result.class_activity_1 = class_activity_1
            result.class_activity_2 = class_activity_2
            result.quiz_1 = quiz_1
            result.quiz_2 = quiz_2
            result.quiz_3 = quiz_3
            result.quiz_4 = quiz_4
            result.save()
            messages.success(request, 'Result Updated!')
            return redirect('add_result')
        else:
            result = Student_Result(
                student_id=get_student,
                subject_id=get_subject,
                assignment_marks=assignment_1,
                assignment_2=assignment_2,
                assignment_3=assignment_3,
                assignment_4=assignment_4,
                exam_marks=exam_marks,
                mid_term=midterm,
                class_activity_1=class_activity_1,
                class_activity_2=class_activity_2,
                quiz_1=quiz_1,
                quiz_2=quiz_2,
                quiz_3=quiz_3,
                quiz_4=quiz_4,
            )
            result.save()
            messages.success(request, 'Result Uploaded!')
            return redirect('add_result')


def STAFF_STATS(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff=staff_id)
    action = request.GET.get('action')

    total_class_activity_sum = 0
    total_students = 0
    average_class_activity = None
    students = None
    activity_avg = None

    if action is not None:
        subject_id = request.POST.get('subject_id')
        get_subject = Subject.objects.get(id=subject_id)
        subjects = Subject.objects.filter(id=subject_id)

        for i in subjects:
            student_id = i.course.id
            students = Student.objects.filter(course_id=student_id)
            students_count = students.count()
            total_students += students_count

            for student in students:
                student_results = Student_Result.objects.filter(
                    subject_id=get_subject,
                    student_id=student
                ).first()

                if student_results:
                    # Calculate individual student's activity average
                    activity_avg = (student_results.class_activity_1 + student_results.class_activity_2) / 2
                    student.activity_avg = activity_avg
                    print(activity_avg)

                    total_class_activity_sum += student_results.class_activity_1
                    total_class_activity_sum += student_results.class_activity_2

        average_class_activity = total_class_activity_sum / total_students if total_students else 0

    context = {
        'subjects': subjects,
        'action': action,
        'average_class_activity': average_class_activity,
        'students': students,
    }
    # staff_id = Staff.objects.get(admin=request.user.id)
    # subjects = Subject.objects.filter(staff=staff_id)
    # action = request.GET.get('action')
    #
    # if action is not None:
    #     subject_id = request.POST.get('subject_id')
    #
    #     get_subject = Subject.objects.get(id=subject_id)
    #     subjects = Subject.objects.filter(id=subject_id)
    #
    #     for i in subjects:
    #         student_id = i.course.id
    #         students = Student.objects.filter(course_id=student_id)
    #
    #         student_results = Student_Result.objects.filter(subject_id=get_subject)
    #         for student_result in student_results:
    #             activity_1 = student_result.class_activity_1
    #             activity_2 = student_result.class_activity_2
    #
    #             avg = activity_1 + activity_2
    #             print(avg)
    #
    # context = {
    #     'subjects': subjects,
    #     'action': action,
    # }

    return render(request, "staff/stats.html", context)


def STUDENT_PROFILE(request, pk):
    student_id = Student.objects.get(id=pk)
    student_results = Student_Result.objects.filter(student_id=student_id)

    assignment_and_quiz = None
    class_activity = None
    mid_term = None
    exam_marks = None

    for student_result in student_results:
        assignment_marks_1 = student_result.assignment_marks
        assignment_marks_2 = student_result.assignment_2
        assignment_marks_3 = student_result.assignment_3
        assignment_marks_4 = student_result.assignment_4
        exam_marks = student_result.exam_marks
        mid_term = student_result.mid_term
        class_activity_1 = student_result.class_activity_1
        class_activity_2 = student_result.class_activity_2
        quiz_1 = student_result.quiz_1
        quiz_2 = student_result.quiz_2
        quiz_3 = student_result.quiz_3
        quiz_4 = student_result.quiz_4
        assignment_and_quiz = assignment_marks_1 + assignment_marks_2 + assignment_marks_3 + assignment_marks_4 + quiz_1 + quiz_2 + quiz_3 + quiz_4
        class_activity = class_activity_1 + class_activity_2

        print(exam_marks, mid_term, class_activity, assignment_and_quiz)

    context = {
        'assignment_and_quiz': assignment_and_quiz,
        'class_activity': class_activity,
        'mid_term': mid_term,
        'exam_marks': exam_marks,
        'student_id': student_id,
    }

    return render(request, 'staff/student_profile.html', context)


def VIDEO_LECTURES(request):
    staff = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff=staff)
    action = request.GET.get('action')

    students = None
    get_subject = None
    syllabus = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')

            get_subject = Subject.objects.get(id=subject_id)
            # subjects = Subject.objects.filter(id=subject_id)
            # for i in subjects:
            #     student_id = i.course.id
            #     students = Student.objects.filter(course_id=student_id)
            syllabus = Syllabus.objects.filter(subject=get_subject)

    context = {
        'subjects': subjects,
        'action': action,
        # 'students': students,
        'get_subject': get_subject,
        'syllabus': syllabus,
    }

    return render(request, 'staff/video_lectures_upload.html', context)


# def STUDENT_VIDEO(request):
#     return render(request, 'staff/student_video.html')


def ADD_TOPIC(request):
    if request.method == "POST":
        week = request.POST.get('week')
        topic = request.POST.get('topic')
        subject_id = request.POST.get('subject_id')
        video_url = request.POST.get('video_url')
        notes = request.POST.get('notes')

        subject = get_object_or_404(Subject, pk=subject_id)

        syllabus = Syllabus(
            week=week,
            topics=topic,
            subject=subject,
            video_link=video_url,
            notes_pdf=notes,
        )
        messages.success(request, "Topic has been added!")
        syllabus.save()

        return redirect('video_lectures_upload')


def DELETE_TOPIC(request, pk):
    syllabus = Syllabus.objects.get(id=pk)
    syllabus.delete()

    return redirect('video_lectures_upload')


def UPDATE_TOPIC_PAGE(request, pk):
    syllabus = Syllabus.objects.get(id=pk)

    context = {
        'syllabus': syllabus,
    }

    return render(request, 'staff/update_topic_page.html', context)


def UPDATE_TOPIC(request, pk):
    if request.method == "POST":
        week = request.POST.get('week')
        topic = request.POST.get('topic')
        subject_id = request.POST.get('subject_id')
        video_url = request.POST.get('video_url')
        notes = request.FILES.get('notes')
        delete_notes = request.POST.get('delete_notes', False)

        syllabus = Syllabus.objects.get(id=pk)

        syllabus.week = week
        syllabus.topics = topic
        syllabus.video_link = video_url
        if notes is not None and notes is not "":
            syllabus.notes_pdf = notes
        elif delete_notes and syllabus.notes_pdf:
            file_path = os.path.join(settings.MEDIA_ROOT, str(syllabus.notes_pdf))
            os.remove(file_path)
            syllabus.notes_pdf.delete(save=False)

        messages.success(request, 'Topic is successfully updated!')
        syllabus.save()

        # return redirect('update_topic_page', pk=pk)
        return redirect('video_lectures_upload')


def DIARY(request):
    staff = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff=staff)
    action = request.GET.get('action')

    get_subject = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')

            get_subject = Subject.objects.get(id=subject_id)

    context = {
        'subjects': subjects,
        'action': action,
        'get_subject': get_subject,
    }

    return render(request, 'staff/diary.html', context)


def ADD_DIARY(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        diary_date = request.POST.get('diary_date')
        diary = request.POST.get('diary')

        subject = Subject.objects.get(id=subject_id)

        daily_diary = Diary(
            subject=subject,
            diary_date=diary_date,
            diary=diary,
        )
        messages.success(request, 'Diary Uploaded!')
        daily_diary.save()

        return redirect('diary')


def CHECK_SCHEDULE(request):
    staff = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff=staff)
    action = request.GET.get('action')

    get_subject = None
    schedule = None

    if action is not None:
        subject_id = request.POST.get('subject_id')
        get_subject = Subject.objects.get(id=subject_id)

        schedule = Schedule.objects.filter(staff=staff, subject=get_subject)

    context = {
        'subjects': subjects,
        'action': action,
        'get_subject': get_subject,
        'schedule': schedule,
    }

    return render(request, 'staff/check_schedule.html', context)


@csrf_exempt
def PAPERS(request):
    staff = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff=staff)

    if request.method == 'POST':
        exam_name = request.POST.get('exam_name')
        exam_subject_id = request.POST.get('exam_subject')
        exam_class = request.POST.get('exam_class')
        exam_teacher = request.POST.get('exam_teacher')
        exam_time = request.POST.get('exam_time')
        exam_time_end = request.POST.get('exam_time_end')
        exam_question = request.POST.get('exam_question')

        exam_subject = Subject.objects.get(id=exam_subject_id)

        # Create a response object with a PDF MIME type
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{exam_name}.pdf"'

        # Create a PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)

        # Create a list for the PDF content
        content = []

        # Get sample styles from ReportLab
        styles = getSampleStyleSheet()

        # Define your custom styles or modify existing ones
        custom_style = styles['Normal']
        custom_style.leading = 16  # Adjust line spacing if needed

        # Create paragraphs using your content and styles
        content.append(Paragraph(f'<b>Exam Name:</b> {exam_name}', custom_style))
        content.append(Paragraph(f'<b>Exam Subject:</b> {exam_subject.name}', custom_style))
        content.append(Paragraph(f'<b>Exam Class:</b> {exam_class}', custom_style))
        content.append(Paragraph(f'<b>Exam Teacher:</b> {exam_teacher}', custom_style))
        content.append(Paragraph(f'<b>Exam Time:</b> {exam_time} To {exam_time_end}', custom_style))
        content.append(Paragraph('<b>Exam Question:</b>', custom_style))
        content.append(Paragraph(exam_question, custom_style))

        doc.build(content)

        pdf_data = response.getvalue()  # Get the PDF data
        new_pdf = ExamPaper(
            exam_name=exam_name,
            exam_subject=exam_subject,
            exam_class=exam_class,
            exam_teacher=exam_teacher,
            exam_time=exam_time,
            exam_time_end=exam_time_end,
            exam_question=exam_question,
            pdf_content=pdf_data
        )
        new_pdf.save()

        return response

    context = {
        'subjects': subjects,
        'staff': staff,
    }

    return render(request, 'staff/papers.html', context)


def VIEW_PAPER(request):
    staff = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff=staff)
    papers = ExamPaper.objects.filter(exam_subject__in=subjects)
    # for subject in subjects:
    #     papers = ExamPaper.objects.filter(exam_subject=subject)
    #     for paper in papers:
    context = {
        'papers': papers,
    }

    return render(request, 'staff/view_paper.html', context)


def EDIT_PAPER(request, pk):
    staff = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff=staff)

    paper = ExamPaper.objects.get(id=pk)

    context = {
        'paper': paper,
        'subjects': subjects,
    }

    return render(request, 'staff/edit_paper.html', context)


# def UPDATE_PAPER(request, pk):
#     if request.method == 'POST':
#         exam_name = request.POST.get('exam_name')
#         exam_subject_id = request.POST.get('exam_subject')
#         exam_class = request.POST.get('exam_class')
#         exam_teacher = request.POST.get('exam_teacher')
#         exam_time = request.POST.get('exam_time')
#         exam_time_end = request.POST.get('exam_time_end')
#         exam_question = request.POST.get('exam_question')
#
#         # exam_subject = Subject.objects.get(id=exam_subject_id)
#
#         paper = ExamPaper.objects.get(id=pk)
#
#         paper.exam_name = exam_name
#         # paper.exam_subject = exam_subject
#         paper.exam_class = exam_class
#         paper.exam_teacher = exam_teacher
#         paper.exam_time = exam_time
#         paper.exam_time_end = exam_time_end
#         paper.exam_question = exam_question
#         paper.save()
#
#     return redirect('view_paper')

@csrf_exempt
def UPDATE_PAPER(request, pk):
    paper = ExamPaper.objects.get(id=pk)

    if request.method == 'POST':
        exam_name = request.POST.get('exam_name')
        exam_subject_id = int(request.POST.get('exam_subject'))
        exam_class = request.POST.get('exam_class')
        exam_teacher = request.POST.get('exam_teacher')
        exam_time = request.POST.get('exam_time')
        exam_time_end = request.POST.get('exam_time_end')
        exam_question = request.POST.get('exam_question')

        exam_subject = Subject.objects.get(id=exam_subject_id)

        paper = ExamPaper.objects.get(id=pk)

        paper.exam_name = exam_name
        paper.exam_subject = exam_subject
        paper.exam_class = exam_class
        paper.exam_teacher = exam_teacher
        paper.exam_time = exam_time
        paper.exam_time_end = exam_time_end
        paper.exam_question = exam_question

        # Generate a new PDF with the updated information
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{exam_name}.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []

        custom_style = styles['Normal']
        custom_style.leading = 16

        content.append(Paragraph(f'<b>Exam Name:</b> {exam_name}', custom_style))
        content.append(Paragraph(f'<b>Exam Subject:</b> {exam_subject.name}', custom_style))
        content.append(Paragraph(f'<b>Exam Class:</b> {exam_class}', custom_style))
        content.append(Paragraph(f'<b>Exam Teacher:</b> {exam_teacher}', custom_style))
        content.append(Paragraph(f'<b>Exam Time:</b> {exam_time} To {exam_time_end}', custom_style))
        content.append(Paragraph('<b>Exam Question:</b>', custom_style))
        content.append(Paragraph(exam_question, custom_style))

        doc.build(content)

        pdf_data = response.getvalue()
        paper.pdf_content = pdf_data

        paper.save()

        return response

    return redirect('view_paper')


def NOTICEBOARD(request):
    notices = NoticeBoard_Teachers.objects.all()

    context = {
        'notices': notices,
    }

    return render(request, 'staff/noticeboard.html', context)
