from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Enrollment, CourseMaterial
from django.contrib.auth import get_user_model
from .decorators import role_required

@login_required
def dashboard(request):
    context = {'role': request.user.role}
    if request.user.role == 'student':
        context['enrolled_courses'] = Enrollment.objects.filter(student=request.user)
    elif request.user.role == 'teacher':
        context['my_courses'] = Course.objects.filter(teacher=request.user)
    elif request.user.role == 'admin':
        User = get_user_model()
        context['total_courses'] = Course.objects.count()
        context['total_users'] = User.objects.count()
        context['total_students'] = User.objects.filter(role='student').count()
        context['total_teachers'] = User.objects.filter(role='teacher').count()
    return render(request, 'dashboard.html', context)

@login_required
@role_required(['student'])
def register_for_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, f'Successfully registered for {course.name}')
    else:
        messages.info(request, 'Already registered for this course')
    return redirect('my_courses')

@login_required
@role_required(['student', 'teacher'])
def my_courses(request):
    if request.user.role == 'student':
        enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
        courses = [e.course for e in enrollments]
    else:  # teacher
        courses = Course.objects.filter(teacher=request.user)
    return render(request, 'my_courses.html', {'courses': courses})

@login_required
@role_required(['student', 'teacher'])
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = CourseMaterial.objects.filter(course=course)
    return render(request, 'course_detail.html', {'course': course, 'materials': materials})

@login_required
@role_required(['teacher'])
def upload_material(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        if title and file:
            CourseMaterial.objects.create(course=course, title=title, file=file, uploaded_by=request.user)
            messages.success(request, 'Material uploaded successfully')
            return redirect('course_detail', course_id=course.id)
    return render(request, 'upload_material.html', {'course': course})

@login_required
@role_required(['admin'])
def manage_courses(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            Course.objects.create(name=name, description=description)
            messages.success(request, 'Course created successfully')
    courses = Course.objects.all()
    return render(request, 'manage_course.html', {'courses': courses})

@login_required
@role_required(['admin'])
def assign_teacher(request):
    courses = Course.objects.filter(teacher__isnull=True)
    teachers = CustomUser.objects.filter(role='teacher')
    
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        teacher_id = request.POST.get('teacher_id')
        course = get_object_or_404(Course, id=course_id)
        teacher = get_object_or_404(CustomUser, id=teacher_id)
        course.teacher = teacher
        course.save()
        messages.success(request, f'Teacher assigned to {course.name}')
        return redirect('assign_teacher')
    
    return render(request, 'assign_teacher.html', {'courses': courses, 'teachers': teachers})