from _decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render, redirect
from schoolsystem.models import Student_Notification, Student, Student_Feedback, Student_Leave, Subject, Attendance, \
    Attendance_Report, Student_Result, Diary, Syllabus, Schedule, NoticeBoard_Students, Student_Support, \
    Student_Support_Reply, Invoice, InvoiceItem
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
import uuid


def HOME(request):
    return render(request, 'student/home.html')


def NOTIFICATIONS(request):
    student = Student.objects.filter(admin=request.user.id)
    for i in student:
        student_id = i.id

        notification = Student_Notification.objects.filter(student_id=student_id)

        context = {
            'notification': notification,
        }

    return render(request, 'student/notification.html', context)


def STUDENT_NOTIFICATION_MARK_AS_DONE(request, status):
    notification = Student_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('student_notifications')


def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin=request.user.id)

    feedback_history = Student_Feedback.objects.filter(student_id=student_id)

    context = {
        'feedback_history': feedback_history,
    }

    return render(request, 'student/feedback.html', context)


def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        student = Student.objects.get(admin=request.user.id)

        student_feedback = Student_Feedback(
            student_id=student,
            feedback=feedback,
            feedback_reply='',
        )
        student_feedback.save()
        messages.success(request, 'Feedback has been sent!')

        return redirect('student_feedback')


def STUDENT_LEAVE(request):
    student = Student.objects.get(admin=request.user.id)
    student_id = student.id

    leave_history = Student_Leave.objects.filter(student_id=student_id)

    context = {
        'leave_history': leave_history,
    }

    return render(request, 'student/apply_leave.html', context)


def STUDENT_LEAVE_SEND(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student = Student.objects.get(admin=request.user.id)

        leave = Student_Leave(
            student_id=student,
            date=leave_date,
            message=leave_message,
        )
        leave.save()
        messages.success(request, 'Leave Sent!')
        return redirect('student_apply_leave')


def STUDENT_VIEW_ATTENDANCE(request):
    student = Student.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(course=student.course_id)
    action = request.GET.get('action')

    get_subject = None
    attendance_report = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)

            # attendance = Attendance.objects.get(subject_id=get_subject)
            attendance_report = Attendance_Report.objects.filter(student_id=student,
                                                                 attendance_id__subject_id=subject_id)

    context = {
        'subject': subject,
        'action': action,
        'get_subject': get_subject,
        'attendance_report': attendance_report,
    }

    return render(request, 'student/view_attendance.html', context)


def VIEW_RESULT(request):
    marks = None
    assignment = None
    student = Student.objects.get(admin=request.user.id)

    results = Student_Result.objects.filter(student_id=student)

    for result in results:
        total_marks = (
                result.assignment_marks + result.assignment_2 + result.assignment_3 + result.assignment_4 +
                result.exam_marks + result.mid_term + result.class_activity_1 + result.class_activity_2 +
                result.quiz_1 + result.quiz_2 + result.quiz_3 + result.quiz_4
        )
        result.total_marks = total_marks

    context = {
        'results': results,
    }

    return render(request, 'student/view_result.html', context)


def VIEW_DIARY(request):
    student = Student.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(course=student.course_id)
    action = request.GET.get('action')

    get_subject = None
    diaries = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)

            diaries = Diary.objects.filter(subject=get_subject)

    context = {
        'subject': subject,
        'action': action,
        'get_subject': get_subject,
        'diaries': diaries,
    }

    return render(request, 'student/view_diary.html', context)


def CHECK_DIARY(request, subject_id, diary_date):
    subject = get_object_or_404(Subject, id=subject_id)
    diary = get_object_or_404(Diary, subject_id=subject_id, diary_date=diary_date)

    context = {
        'get_subject': subject,
        'diary': diary,
    }

    return render(request, 'student/check_diary.html', context)


def VIDEO_LECTURE(request):
    student = Student.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(course=student.course_id)
    action = request.GET.get('action')

    get_subject = None
    syllabus = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)

            syllabus = Syllabus.objects.filter(subject=get_subject)

    context = {
        'subject': subject,
        'action': action,
        'get_subject': get_subject,
        'syllabus': syllabus,
    }

    return render(request, 'student/video_lecture.html', context)


def CLASS_TIMETABLE(request):
    student = Student.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(course=student.course_id)

    all_schedules = []

    for subject in subjects:
        schedules = Schedule.objects.filter(subject=subject)
        all_schedules.extend(list(schedules))

    context = {
        'schedules': all_schedules,
    }

    return render(request, 'student/class_timetable.html', context)


def NOTICEBOARD(request):
    notices = NoticeBoard_Students.objects.all()

    context = {
        'notices': notices,
    }

    return render(request, 'student/noticeboard.html', context)


def STUDENT_SUPPORT(request):
    student = Student.objects.get(admin=request.user.id)

    if request.method == "POST":
        name = student
        subject = request.POST.get('subject')
        query = request.POST.get('query')

        support = Student_Support(
            name=name,
            subject=subject,
            any_query=query,
        )
        support.save()
        messages.success(request, 'Query has been Sent!')
        return redirect('student_support')

    context = {
        'student': student,
    }

    return render(request, 'student/student_support.html', context)


def INBOX(request):
    student = Student.objects.get(admin=request.user.id)
    support_queries = Student_Support.objects.filter(name=student)

    # support = Student_Support_Reply.objects.filter(subject__in=support_queries)

    # Fetch associated replies for each query
    support_data = []
    for query in support_queries:
        replies = query.replies.all()  # Use the correct reverse relation name
        support_data.append({'query': query, 'replies': replies})

    context = {
        'support_data': support_data,
    }

    return render(request, 'student/inbox.html', context)


def SUPPORT_REPLY(request, pk):
    # try:
    #     support_reply = get_object_or_404(Student_Support_Reply, subject=pk)
    # except Student_Support_Reply.MultipleObjectsReturned:
    support_reply = Student_Support_Reply.objects.filter(subject=pk)

    query = Student_Support.objects.get(id=pk)

    context = {
        'support_reply': support_reply,
        'query': query,
    }

    return render(request, 'student/support_reply.html', context)


def INBOX_DELETE(request, pk):
    inbox = Student_Support.objects.get(id=pk)
    inbox.delete()
    messages.success(request, 'Query has been deleted!')

    return redirect('inbox')


def FEES(request):
    student = Student.objects.get(admin=request.user.id)
    invoice = Invoice.objects.get(course=student.course_id)
    fees = InvoiceItem.objects.filter(invoice=invoice)

    context = {
        'fees': fees,
    }

    return render(request, 'student/fees.html', context)


def generate_serial_number(course_id):
    timestamp = int(datetime.timestamp(datetime.now()))
    unique_id = str(uuid.uuid4().int)[:8]  # Using the first 8 characters of a UUID as a unique identifier
    return f'{course_id}_{timestamp}_{unique_id}'


def GENERATE_PDF(request):
    student = Student.objects.get(admin=request.user.id)
    invoice = Invoice.objects.get(course=student.course_id)
    items = InvoiceItem.objects.filter(invoice=invoice)
    date = datetime.now()
    print(date)

    # Update serial number for the invoice
    invoice.serial_number = generate_serial_number(invoice.course.id)
    invoice.save()

    fee_total = InvoiceItem.objects.filter(invoice=invoice).aggregate(total_amount=Sum('amount'))
    total_amount = fee_total['total_amount'] or Decimal(0)

    # for i in items:
    #     amt = i.amount
    #     total = sum(amt)
    #     print(total)

    context = {
        'invoice': invoice,
        'items': items,
        'date': date,
        'total_amount': total_amount,
    }

    template_path = 'student/invoice_template_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'

    pisa_status = pisa.CreatePDF(
        html, dest=response,
    )

    if pisa_status.err:
        return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisa_status.err, html))

    return response
