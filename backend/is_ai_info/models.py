from django.conf import settings
from django.db import models


class UserDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    email = models.EmailField()

    class Meta:
        abstract = True


class Group(models.Model):
    group_name = models.CharField(max_length=7, verbose_name='Номер группы')


class Student(UserDetail):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Educator(UserDetail):
    ASSISTANT = "AS"
    SENIOR_TEACHER = "ST"
    DOCENT = "DC"
    PROFESSOR = "PR"
    ACADEMIC_DEGREES = [
        (ASSISTANT, 'Ассистент'),
        (SENIOR_TEACHER, 'Старший преподаватель'),
        (DOCENT, 'Доцент'),
        (PROFESSOR, 'Профессор')
    ]
    academic_degree = models.CharField(max_length=2, choices=ACADEMIC_DEGREES, verbose_name='Учёная степень')
    department_head = models.BooleanField(default=False, verbose_name='Заведующий кафедрой')


class Subject(models.Model):
    subject_name = models.CharField(max_length=80)


class SubjectInSchedule(models.Model):
    FIRST = "08:30-10:00"
    SECOND = "10:10-11:40"
    THIRD = "11:50-13:20"
    FOURTH = "13:50-15:20"
    FIFTH = "15:30-17:00"
    SIXTH = "17:10-18:40"
    SEVENTH = "18:50-20:20"
    EIGHTH = "20:30-22:00"

    TIME = [
        (FIRST, 'Первая пара'),
        (SECOND, 'Вторая пара'),
        (THIRD, 'Третья пара'),
        (FOURTH, 'Четвёртая пара'),
        (FIFTH, 'Пятая пара'),
        (SIXTH, 'Шестая пара'),
        (SEVENTH, 'Седьмая пара'),
        (EIGHTH, 'Восьмая пара'),
    ]

    MONDAY = "MON"
    TUESDAY = "TUE"
    WEDNESDAY = "WED"
    THURSDAY = "THU"
    FRIDAY = "FRI"
    SATURDAY = "SAT"

    WORKDAYS = [
        (MONDAY, 'Понедельник'),
        (TUESDAY, 'Вторник'),
        (WEDNESDAY, 'Среда'),
        (THURSDAY, 'Четверг'),
        (FRIDAY, 'Пятница'),
        (SATURDAY, 'Суббота'),
    ]

    educator = models.ForeignKey(Educator, on_delete=models.CASCADE)
    from_to = models.CharField(max_length=11, choices=TIME, verbose_name='Порядок пары')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=WORKDAYS, verbose_name='День недели')
    # тру - чётная, фолс - нечётная
    even_week = models.BooleanField(verbose_name='Четная неделя')


class Question(models.Model):
    question_from = models.ForeignKey(Student, on_delete=models.SET_NULL)
    question_to = models.ForeignKey(Educator, on_delete=models.SET_NULL)
    is_private = models.BooleanField(default=False)
    text = models.TextField()
    question_datetime = models.DateTimeField(auto_now_add=True)


class QuestionReply(models.Model):
    author_educator = models.ForeignKey(Educator, on_delete=models.SET_NULL, default=None)
    author_student = models.ForeignKey(Student, on_delete=models.SET_NULL, default=None)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    reply_datetime = models.DateTimeField(auto_now_add=True)
