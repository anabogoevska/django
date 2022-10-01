import uuid
from django.urls import reverse
from audioop import reverse as audio_reverse
from email.policy import default
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models


# Create your models here.



class Course(models.Model):
    course_name = models.CharField(max_length=150)
    cover_image=models.ImageField(upload_to="cover_images", null=True, blank=True)
    number_of_lesson = models.IntegerField()
    average_time = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, default=uuid.uuid1)

    class Meta:
       ordering=('-course_name',)
    def __str__(self):
       return self.course_name

    def get_absolute_url(self):
        return reverse('lesson:lesson_by_category', args=[self.slug])

    @staticmethod
    def get_all_courses():
        return Course.objects.all()

class Lesson(models.Model):
    lesson_name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=uuid.uuid1)
    content = models.TextField(default='null')
    image = models.ImageField(upload_to="cover_images", null=True, blank=True)

    class Meta:
        ordering=('-lesson_name',)

    @staticmethod
    def get_all_lessons():
        return Lesson.objects.all()

    @staticmethod
    def get_all_lessons_by_course_name(course_name):
        if course_name:
            return Course.objects.all(course=course_name)
        else:
            return Lesson.get_all_lessons()

    def __str__(self):
        return self.lesson_name









