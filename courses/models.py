from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'role': 'teacher'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student.username} - {self.course.name}"

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title