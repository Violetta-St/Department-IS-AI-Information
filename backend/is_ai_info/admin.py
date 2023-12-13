from django.contrib import admin

from .models import *

admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Educator)
admin.site.register(Subject)
admin.site.register(SubjectInSchedule)
admin.site.register(Question)
admin.site.register(QuestionReply)
